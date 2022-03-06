import unittest
from unittest import mock

from linebot import models

from src.app.text_handlers.text_handlers import (
    DefaultTextMessageHandler,
    ProductUrlTextMessageHandler,
    ProductListTextMessageHandler,
)
from src.shared.uq.uq_product import UqProductException


class TestDefaultTextMessageHandler(unittest.TestCase):
    def test_execute_should_generate_help_message(self):
        handler = DefaultTextMessageHandler("any message", "user_id")

        response_message = handler.execute()

        self.assertIsInstance(response_message, models.Message)
        self.assertEqual(response_message.text, "請傳送商品網址")


class TestProductUrlTextMessageHandler(unittest.TestCase):
    """
    Not to mock UqProductCodeParser since two reasons, 1) no side effect and
    2) easier to read as more like a real scenario.
    """

    def test_is_command_should_return_false_if_no_product_code_found_from_text(self):
        result = ProductUrlTextMessageHandler.is_command("Not a URL")

        self.assertEqual(False, result)

    def test_is_command_should_return_true_if_product_code_found_from_text(self):
        result = ProductUrlTextMessageHandler.is_command(
            "https://m.uniqlo.com/tw/product?pid=u0000000009993"
        )

        self.assertEqual(True, result)

    @mock.patch("src.app.text_handlers.text_handlers.UqProduct", autospec=True)
    @mock.patch("src.app.text_handlers.text_handlers.UqRetriever", autospec=True)
    @mock.patch("requests.Session", autospec=True)
    def test_execute_should_return_confirmation_template_message(
        self, mock_requests, mock_retriever, mock_product
    ):
        uq_product = mock.MagicMock()
        uq_product.name = "name"
        uq_product.product_code = "u0000000009993"
        uq_product.special_offer = 100
        mock_product.return_value = uq_product

        handler = ProductUrlTextMessageHandler(
            "https://m.uniqlo.com/tw/product?pid=u0000000009993", "user_id"
        )
        message = handler.execute()

        self.assertIsInstance(message, models.TemplateSendMessage)

    @mock.patch("src.app.text_handlers.text_handlers.UqProduct", autospec=True)
    @mock.patch(
        "src.app.text_handlers.text_handlers.UqRetriever",
        autospec=True,
        side_effect=UqProductException,
    )
    @mock.patch("requests.Session", autospec=True)
    def test_execute_should_return_product_code_error_message_if_product_not_found(
        self, mock_requests, mock_retriever, mock_product
    ):
        handler = ProductUrlTextMessageHandler(
            "https://m.uniqlo.com/tw/product?pid=nothing", "user_id"
        )
        message = handler.execute()

        self.assertIsInstance(message, models.TextMessage)

    class TestProductListTextMessageHandler(unittest.TestCase):
        def test_is_command_should_return_true_if_matches_condition(self):
            result = ProductListTextMessageHandler.is_command("管理個人清單")

            self.assertEqual(result, True)

        def test_is_command_should_return_false_if_not_matches_condition(self):
            result = ProductListTextMessageHandler.is_command("Not matched")

            self.assertEqual(result, False)

        @mock.patch(
            "src.app.text_handlers.text_handlers.UserDataRetriever", autospec=True
        )
        @mock.patch("src.app.text_handlers.text_handlers.User", autospec=True)
        def test_is_command_should_return_no_subscribed_product_message_if_no_product(
            self, mock_user, mock_user_data_retriever
        ):
            user = mock.MagicMock()
            mock_user.get_or_create.return_value = (user, False)
            user_data_retriever = mock_user_data_retriever.return_value
            user_data_retriever.get_subscribed_products = {}

            handler = ProductListTextMessageHandler("管理個人清單", "user_id")
            result = handler.execute()

            self.assertEqual(result.text, "你沒有追蹤中的商品喔！")

        @mock.patch("src.app.text_handlers.text_handlers.UqProduct", autospec=True)
        @mock.patch("src.app.text_handlers.text_handlers.UqRetriever", autospec=True)
        @mock.patch("requests.Session", autospec=True)
        @mock.patch(
            "src.app.text_handlers.text_handlers.UserDataRetriever", autospec=True
        )
        @mock.patch("src.app.text_handlers.text_handlers.User", autospec=True)
        def test_is_command_should_return_product_management_message(
            self,
            mock_user,
            mock_user_data_retriever,
            mock_session,
            mock_uq_retriever,
            mock_uq_product,
        ):
            user = mock.MagicMock()
            mock_user.get_or_create.return_value = (user, False)
            user_data_retriever = mock_user_data_retriever.return_value
            user_data_retriever.get_subscribed_products = {
                "product1": mock.MagicMock(),
                "product2": mock.MagicMock(),
            }
            uq_product1 = mock.MagicMock()
            uq_product1.name = "product1"
            uq_product1.is_on_sale = True
            uq_product1.original_price = 100
            uq_product1.special_offer = 50
            uq_product1.website_url = "https://whatever.com"
            uq_product2 = mock.MagicMock()
            uq_product2.name = "product2"
            uq_product2.is_on_sale = False
            uq_product2.original_price = 100
            uq_product2.special_offer = 100
            uq_product2.website_url = "https://whatever.com"
            mock_uq_product.reset_mock(side_effect=[uq_product1, uq_product2])

            handler = ProductListTextMessageHandler("管理個人清單", "user_id")
            result = handler.execute()

            self.assertIsInstance(result, models.TemplateSendMessage)
