import unittest
from unittest import mock

from linebot import models

from src.shared.line.message_creators.template_message_creators import (
    UqProductSubscriptionConfirmationMessageCreator,
    UqProductManagementTemplateMessageCreator,
)
from src.shared.line.postback_action_models import ProductAddingConfirmationDataModel


class TestUqProductSubscriptionConfirmationMessageCreator(unittest.TestCase):
    def test_product_subscription_confirmation_message_should_contain_product_info(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.special_offer = 100

        creator = UqProductSubscriptionConfirmationMessageCreator(product1)
        message = creator.generate()

        self.assertEqual("product1", message.template.title)
        self.assertEqual("NT $100\n你要追蹤此商品嗎？", message.template.text)

    def test_product_subscription_confirmation_message_should_contain_yes_and_no_actions(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.special_offer = 100

        creator = UqProductSubscriptionConfirmationMessageCreator(product1)
        message = creator.generate()
        yes_action = message.template.actions[0]
        no_action = message.template.actions[1]

        self.assertIsInstance(yes_action, models.PostbackAction)
        self.assertIsInstance(no_action, models.MessageAction)

    def test_product_subscription_confirmation_message_yes_action_should_contain_correct_postback_data(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.special_offer = 100

        creator = UqProductSubscriptionConfirmationMessageCreator(product1)
        message = creator.generate()
        yes_action = message.template.actions[0]
        postback_data = ProductAddingConfirmationDataModel.parse_raw(yes_action.data)

        self.assertEqual("add", postback_data.action)
        self.assertEqual("product_code1", postback_data.product_code)


class TestUqProductManagementTemplateMessageCreator(unittest.TestCase):
    """
    We don't mock the factory class and UqProductManagementTemplateColumnCreator
    because the flow is relatively simple. By testing with real dependencies, we
    can catch the bug earlier.
    """

    def test_generated_carousel_template_message_should_contain_product_columns(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.is_on_sale = False
        product1.original_price = 100
        product2 = mock.MagicMock()
        product2.name = "product2"
        product2.product_code = "product_code2"
        product2.website_url = "https://abcd.com/product2"
        product2.is_on_sale = False
        product2.original_price = 200

        creator = UqProductManagementTemplateMessageCreator([product1, product2])
        message = creator.generate()
        column1 = message.template.columns[0]
        column2 = message.template.columns[1]

        self.assertEqual(2, len(message.template.columns))
        self.assertEqual("product1", column1.title)
        self.assertEqual("product2", column2.title)
