import unittest
from unittest import mock

from linebot import models

from src.shared.line.product_subscription import (
    UqProductSubscriptionConfirmationMessageCreator,
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
        message = creator.generate_product_subscription_confirmation_message()

        self.assertEquals("product1", message.template.title)
        self.assertEquals("NT $100\n你要追蹤此商品嗎？", message.template.text)

    def test_product_subscription_confirmation_message_should_contain_yes_and_no_actions(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.special_offer = 100

        creator = UqProductSubscriptionConfirmationMessageCreator(product1)
        message = creator.generate_product_subscription_confirmation_message()
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
        message = creator.generate_product_subscription_confirmation_message()
        yes_action = message.template.actions[0]
        postback_data = ProductAddingConfirmationDataModel.parse_raw(yes_action.data)

        self.assertEquals("add", postback_data.action)
        self.assertEquals("product_code1", postback_data.product_code)
