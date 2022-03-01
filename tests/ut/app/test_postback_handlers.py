from typing import Type
import unittest
from unittest import mock

from linebot import models

from src.app.postback_handlers import (
    ProductSubscriptionPostbackHandler,
    ProductRemovalPostbackHandler,
)
from src.shared.line.postback_action_models import (
    ProductAddingConfirmationDataModel,
    PostbackDataException,
    ProductRemovalPostbackDataModel,
)


class TestProductSubscriptionPostbackHandler(unittest.TestCase):
    def test_product_adding_confirmation_data_model_is_used_to_parse_data(self):
        data = ProductAddingConfirmationDataModel(product_code="code")

        handler = ProductSubscriptionPostbackHandler(data.json(), "user_id")

        self.assertEqual(handler._data.action, "add")
        self.assertEqual(handler._data.product_code, "code")

    def test_init_should_raise_postback_data_exception_if_validation_failed(self):
        with self.assertRaises(PostbackDataException):
            ProductSubscriptionPostbackHandler("wrong data", "user_id")

    @mock.patch("src.app.postback_handlers.UserDataRetriever")
    @mock.patch("src.app.postback_handlers.User")
    def test_execute_should_return_product_in_list_message_if_product_to_add_already_in_list(
        self, mock_user: Type[mock.MagicMock], mock_retriever: Type[mock.MagicMock]
    ):
        """
        We didn't mock ProductAlreadyInListMessageCreator since 1) testing return value is
        easier to maintain than testing interaction and 2) the side effect of the class is
        limited.
        """
        # set up mock User to return a dummy user object
        dummy_user = mock.MagicMock()
        mock_user.get_or_create.return_value = (dummy_user, False)
        # set up mock get_subscribed_products of UserDataRetriever class
        user_data_retriever_instance = mock.MagicMock()
        product1 = mock.MagicMock()
        product1.name = "product1"
        user_data_retriever_instance.get_subscribed_products.return_value = {
            "product1": product1,
        }
        mock_retriever.return_value = user_data_retriever_instance
        # prepare postback data
        data = ProductAddingConfirmationDataModel(product_code="product1")

        response = ProductSubscriptionPostbackHandler(data.json(), "user_id").execute()

        self.assertIsInstance(response, models.TextMessage)
        self.assertEqual(response.text, "product1已經在你的追蹤清單了喔！")

    @mock.patch("src.app.postback_handlers.UserProduct")
    @mock.patch("src.app.postback_handlers.Product")
    @mock.patch("src.app.postback_handlers.UqProduct")
    @mock.patch("src.app.postback_handlers.UqRetriever")
    @mock.patch("requests.Session")
    @mock.patch("src.app.postback_handlers.UserDataRetriever")
    @mock.patch("src.app.postback_handlers.User")
    def test_execute_should_succeful_operation_if_correctly_adding_the_product_to_list(
        self,
        mock_user: Type[mock.MagicMock],
        mock_user_data_retriever: Type[mock.MagicMock],
        mock_session: Type[mock.MagicMock],
        mock_uq_retriever: Type[mock.MagicMock],
        mock_uq_product: Type[mock.MagicMock],
        mock_product: Type[mock.MagicMock],
        mock_user_product: Type[mock.MagicMock],
    ):
        """
        We didn't mock ProductSuccessfullyAddedMessageCreator since 1) testing return value is
        easier to maintain than testing interaction and 2) the side effect of the class is
        limited.
        """
        dummy_user = mock.MagicMock()
        mock_user.get_or_create.return_value = (dummy_user, False)
        # set up mock get_subscribed_products of UserDataRetriever class
        user_data_retriever_instance = mock.MagicMock()
        user_data_retriever_instance.get_subscribed_products.return_value = {}
        mock_user_data_retriever.return_value = user_data_retriever_instance
        # set up UqProduct data
        dummy_uq_product = mock.MagicMock()
        dummy_uq_product.configure_mock(
            product_code="product_code",
            name="name",
            current_price=100,
            original_price=50,
            short_description="short_description",
        )
        mock_uq_product.return_value = dummy_uq_product
        # Set up get_or_create of Product class
        dummy_product = mock.MagicMock()
        dummy_product.name = "name"
        mock_product.get_or_create.return_value = (dummy_product, False)
        # prepare postback data
        data = ProductAddingConfirmationDataModel(product_code="product_code")

        response = ProductSubscriptionPostbackHandler(data.json(), "user_id").execute()

        self.assertIsInstance(response, models.TextMessage)
        self.assertEqual(response.text, "已成功將name加入追蹤清單！")


class TestProductRemovalPostbackHandler(unittest.TestCase):
    def test_product_removal_postback_data_model_is_used_to_parse_data(self):
        data = ProductRemovalPostbackDataModel(product_code="code")

        handler = ProductSubscriptionPostbackHandler(data.json(), "user_id")

        self.assertEqual(handler._data.action, "remove")
        self.assertEqual(handler._data.product_code, "code")

    @mock.patch("src.app.postback_handlers.UserDataRetriever")
    @mock.patch("src.app.postback_handlers.User")
    def test_execute_should_return_product_not_in_list_yet_message_if_product_not_in_list_yet(
        self, mock_user: Type[mock.MagicMock], mock_retriever: Type[mock.MagicMock]
    ):
        """
        We didn't mock ProductNotInListYetMessageCreator since 1) testing return value is
        easier to maintain than testing interaction and 2) the side effect of the class is
        limited.
        """
        # set up mock User to return a dummy user object
        dummy_user = mock.MagicMock()
        mock_user.get_or_create.return_value = (dummy_user, False)
        # set up mock get_subscribed_products of UserDataRetriever class
        user_data_retriever_instance = mock.MagicMock()
        user_data_retriever_instance.get_subscribed_products.return_value = {}
        mock_retriever.return_value = user_data_retriever_instance
        # prepare postback data
        data = ProductRemovalPostbackDataModel(product_code="product1")

        response = ProductRemovalPostbackHandler(data.json(), "user_id").execute()

        self.assertIsInstance(response, models.TextMessage)
        self.assertEqual(response.text, "你還沒追蹤此商品喔！")

    @mock.patch("src.app.postback_handlers.UserProduct")
    @mock.patch("src.app.postback_handlers.Product")
    @mock.patch("src.app.postback_handlers.UserDataRetriever")
    @mock.patch("src.app.postback_handlers.User")
    def test_execute_should_return_successful_operation_message_if_correctly_removing_the_product_from_list(
        self,
        mock_user: Type[mock.MagicMock],
        mock_user_data_retriever: Type[mock.MagicMock],
        mock_product: Type[mock.MagicMock],
        mock_user_product: Type[mock.MagicMock],
    ):
        """
        We didn't mock ProductSuccessfullyRemovedMessageCreator since 1) testing return value is
        easier to maintain than testing interaction and 2) the side effect of the class is
        limited.
        """
        dummy_user = mock.MagicMock()
        mock_user.get_or_create.return_value = (dummy_user, False)
        # set up mock get_subscribed_products of UserDataRetriever class
        user_data_retriever_instance = mock.MagicMock()
        product1 = mock.MagicMock()
        product1.name = "product1"
        user_data_retriever_instance.get_subscribed_products.return_value = {
            "product1": product1,
        }
        mock_user_data_retriever.return_value = user_data_retriever_instance
        # prepare postback data
        data = ProductRemovalPostbackDataModel(product_code="product1")

        response = ProductRemovalPostbackHandler(data.json(), "user_id").execute()

        self.assertIsInstance(response, models.TextMessage)
        self.assertEqual(response.text, "已成功將product1從清單移除！")
