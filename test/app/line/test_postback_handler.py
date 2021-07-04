import asyncio
from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.line.data_models import UserSource
from app.line.postback_data import PostbackDataAdding, PostbackDataDeleting
from app.line.postback_handler import (
    PostbackEventHandlerAdding,
    PostbackEventHandlerDeleting,
    PostbackHandlerFactory,
)
from app.models.User import User


class TestPostbackAddingHandler(TestCase):
    def test_create_postback_event_handler_adding_instance(self):
        adding_postback_data = PostbackDataAdding(product_id="id", product_name="pname")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerAdding.create(
            adding_postback_data.json(), "token", user_data
        )
        self.assertIsInstance(handler, PostbackEventHandlerAdding)
        self.assertEqual(handler.product_id, "id")
        self.assertEqual(handler.product_name, "pname")
        self.assertEqual(handler.reply_token, "token")
        self.assertEqual(handler.user_id, "uid")

    @patch("app.line.postback_handler.data_access")
    def test_adding_duplicate_item(self, mock_access: MagicMock):
        adding_postback_data = PostbackDataAdding(product_id="id", product_name="pname")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerAdding.create(
            adding_postback_data.json(), "token", user_data
        )
        mock_access.has_user.return_value = True
        mock_access.get_user_info.return_value = User(
            user_id="uid", product_tracking={"id"}, count_tracking=1
        )
        handler.manipulate()
        self.assertEqual(handler.response, ("in_list", {"title": "pname"}))

    @patch("app.line.postback_handler.app_config")
    @patch("app.line.postback_handler.data_access")
    def test_exceeding_maximum(self, mock_access: MagicMock, mock_config: MagicMock):
        self.__test_exceeding_maximum_init(mock_access, mock_config)
        adding_postback_data = PostbackDataAdding(product_id="id", product_name="pname")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerAdding.create(
            adding_postback_data.json(), "token", user_data
        )

        handler.manipulate()

        self.assertEqual(handler.response[0], "reach_limit")
        self.assertIsInstance(handler.response[1], dict)

    def __test_exceeding_maximum_init(
        self, mock_access: MagicMock, mock_config: MagicMock
    ):
        mock_access.has_user.return_value = True
        mock_access.get_user_info.return_value = User(
            user_id="uid", product_tracking={"id1"}, count_tracking=1
        )
        mock_config.TRACKING_ITEM_MAXIMUM = 1

    @patch("app.line.postback_handler.data_access")
    def test_adding_new_item(self, mock_access: MagicMock):
        self.__test_adding_new_item_init(mock_access)
        adding_postback_data = PostbackDataAdding(product_id="id", product_name="pname")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerAdding.create(
            adding_postback_data.json(), "token", user_data
        )

        handler.manipulate()

        self.assertEqual(handler.response, ("tracking", {"title": "pname"}))
        mock_access.update_user.assert_called()

    def __test_adding_new_item_init(self, mock_access: MagicMock):
        mock_access.has_user.return_value = True
        mock_access.get_user_info.return_value = User(
            user_id="uid", product_tracking=set(), count_tracking=0
        )
        mock_access.update_user.return_value = ""

    def test_reply_ran_before_manipulate(self):
        adding_postback_data = PostbackDataAdding(product_id="id", product_name="pname")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerAdding.create(
            adding_postback_data.json(), "token", user_data
        )

        with self.assertRaises(RuntimeError):
            asyncio.run(handler.reply_operation_result())

    @patch("app.line.postback_handler.reply")
    @patch("app.line.postback_handler.add_messages")
    @patch("app.line.postback_handler.data_access")
    def test_reply_pure_text_message(
        self, mock_access: MagicMock, mock_messages: MagicMock, mock_reply: MagicMock
    ):
        self.__test_reply_pure_text_message_init(mock_access, mock_messages)
        adding_postback_data = PostbackDataAdding(product_id="id", product_name="pname")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerAdding.create(
            adding_postback_data.json(), "token", user_data
        )
        handler.manipulate()
        asyncio.run(handler.reply_operation_result())

        mock_reply.assert_called_with(
            "token", [{"type": "text", "text": "pname 商品已在你的追蹤清單"}]
        )

    def __test_reply_pure_text_message_init(
        self, mock_access: MagicMock, mock_messages: MagicMock
    ):
        mock_access.has_user.return_value = True
        mock_access.get_user_info.return_value = User(
            user_id="uid", product_tracking={"id"}, count_tracking=1
        )
        mock_messages.messages = {"in_list": "{title} 商品已在你的追蹤清單"}

    @patch("app.line.postback_handler.reply")
    @patch("app.line.postback_handler.add_messages")
    @patch("app.line.postback_handler.data_access")
    def test_reply_complex_message(
        self, mock_access: MagicMock, mock_messages: MagicMock, mock_reply: MagicMock
    ):
        self.__test_reply_complex_message_init(mock_access, mock_messages)
        adding_postback_data = PostbackDataAdding(product_id="id", product_name="pname")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerAdding.create(
            adding_postback_data.json(), "token", user_data
        )
        handler.manipulate()
        asyncio.run(handler.reply_operation_result())

        self.assertEqual(mock_reply.call_args.args[0], "token")
        self.assertIsInstance(mock_reply.call_args.args[1], list)

    def __test_reply_complex_message_init(
        self, mock_access: MagicMock, mock_messages: MagicMock
    ):
        mock_access.has_user.return_value = True
        mock_access.get_user_info.return_value = User(
            user_id="uid", product_tracking={"id1"}, count_tracking=1
        )
        mock_messages.messages = {"in_list": "{title} 商品已在你的追蹤清單"}


class TestPostbackDeletingHandler(TestCase):
    def test_create_postback_event_handler_deleting_instance(self):
        deleting_postback_data = PostbackDataDeleting(product_id="id")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerDeleting.create(
            deleting_postback_data.json(), "token", user_data
        )
        self.assertIsInstance(handler, PostbackEventHandlerDeleting)
        self.assertEqual(handler.product_id, "id")
        self.assertEqual(handler.reply_token, "token")
        self.assertEqual(handler.user_id, "uid")

    @patch("app.line.postback_handler.data_access")
    def test_delete_item_without_user_record(self, mock_access: MagicMock):
        self.__test_delete_item_without_user_record_init(mock_access)
        deleting_postback_data = PostbackDataDeleting(product_id="id")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerDeleting.create(
            deleting_postback_data.json(), "token", user_data
        )
        handler.manipulate()

        self.assertEqual(handler.response, ("no_user", {}))

    def __test_delete_item_without_user_record_init(self, mock_access: MagicMock):
        mock_access.has_user.return_value = False

    @patch("app.line.postback_handler.data_access")
    def test_delete_untracking_item(self, mock_access: MagicMock):
        self.__test_delete_untracking_item_init(mock_access)
        deleting_postback_data = PostbackDataDeleting(product_id="id")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerDeleting.create(
            deleting_postback_data.json(), "token", user_data
        )
        handler.manipulate()

        self.assertEqual(handler.response, ("not_tracking", {}))

    def __test_delete_untracking_item_init(self, mock_access: MagicMock):
        mock_access.has_user.return_value = True
        mock_access.get_user_info.return_value = User(
            user_id="uid", product_tracking=set(), count_tracking=0
        )

    @patch("app.line.postback_handler.data_access")
    def test_delete_tracking_item(self, mock_access: MagicMock):
        self.__test_delete_tracking_item_init(mock_access)
        deleting_postback_data = PostbackDataDeleting(product_id="id")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerDeleting.create(
            deleting_postback_data.json(), "token", user_data
        )
        handler.manipulate()

        mock_access.update_user.assert_called_with(
            User(user_id="uid", product_tracking=set(), count_tracking=0)
        )
        self.assertEqual(handler.response, ("deleted", {}))

    def __test_delete_tracking_item_init(self, mock_access: MagicMock):
        mock_access.has_user.return_value = True
        mock_access.get_user_info.return_value = User(
            user_id="uid", product_tracking={"id"}, count_tracking=1
        )

    @patch("app.line.postback_handler.reply")
    @patch("app.line.postback_handler.delete_messages")
    @patch("app.line.postback_handler.data_access")
    def test_reply_pure_text_message(
        self, mock_access: MagicMock, mock_messages: MagicMock, mock_reply: MagicMock
    ):
        self.__test_reply_pure_text_message_init(mock_access, mock_messages)
        deleting_postback_data = PostbackDataDeleting(product_id="id")
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackEventHandlerDeleting.create(
            deleting_postback_data.json(), "token", user_data
        )
        handler.manipulate()
        asyncio.run(handler.reply_operation_result())

        mock_reply.assert_called_with("token", [{"type": "text", "text": "已停止追蹤此商品。"}])

    def __test_reply_pure_text_message_init(
        self, mock_access: MagicMock, mock_messages: MagicMock
    ):
        mock_access.has_user.return_value = True
        mock_access.get_user_info.return_value = User(
            user_id="uid", product_tracking={"id"}, count_tracking=1
        )
        mock_messages.messages = {"deleted": "已停止追蹤此商品。"}


class TestPostbackHandlerFactory(TestCase):
    def test_create_adding_postback_event_handler(self):
        adding_postback_data = PostbackDataAdding(product_id="id", product_name="pname").json()
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackHandlerFactory.create(adding_postback_data, "token", user_data)
        self.assertIsInstance(handler, PostbackEventHandlerAdding)

    def test_create_deleting_postback_event_handler(self):
        deleting_postback_data = PostbackDataDeleting(product_id="id").json()
        user_data = UserSource(type="user", userId="uid")
        handler = PostbackHandlerFactory.create(deleting_postback_data, "token", user_data)
        self.assertIsInstance(handler, PostbackEventHandlerDeleting)
