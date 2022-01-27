import unittest
from unittest import mock

from linebot import models

from src.shared.line.postback_action_models import ProductRemovalPostbackDataModel
from src.shared.line.product_management import UqProductManagementTemplateMessageCreator


class TestUqProductManagementTemplateMessageCreator(unittest.TestCase):
    def test_generate_products_carousel_template_should_contain_products_info_in_column(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.special_offer = 100
        product2 = mock.MagicMock()
        product2.name = "product2"
        product2.product_code = "product_code2"
        product2.website_url = "https://abcd.com/product2"
        product2.special_offer = 200

        creator = UqProductManagementTemplateMessageCreator([product1, product2])
        message = creator.generate_products_carousel_template_message()
        column1 = message.template.columns[0]
        column2 = message.template.columns[1]

        self.assertEquals(2, len(message.template.columns))
        self.assertEquals("product1", column1.title)
        self.assertEquals("NT $100", column1.text)
        self.assertEquals("product2", column2.title)
        self.assertEquals("NT $200", column2.text)

    def test_products_carousel_template_column_should_contain_go_website_and_removal_actions(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.special_offer = 100

        creator = UqProductManagementTemplateMessageCreator([product1])
        message = creator.generate_products_carousel_template_message()
        column1 = message.template.columns[0]
        go_website_button = column1.actions[0]
        removal_button = column1.actions[1]

        self.assertIsInstance(go_website_button, models.URIAction)
        self.assertIsInstance(removal_button, models.PostbackAction)

    def test_products_carousel_template_column_go_website_button_link_should_be_product_website(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.special_offer = 100

        creator = UqProductManagementTemplateMessageCreator([product1])
        message = creator.generate_products_carousel_template_message()
        column1 = message.template.columns[0]
        go_website_button = column1.actions[0]

        self.assertEquals(product1.website_url, go_website_button.uri)

    def test_products_carousel_template_column_removal_button_link_should_contain_correct_data(
        self,
    ):
        product1 = mock.MagicMock()
        product1.name = "product1"
        product1.product_code = "product_code1"
        product1.website_url = "https://abcd.com/product1"
        product1.special_offer = 100

        creator = UqProductManagementTemplateMessageCreator([product1])
        message = creator.generate_products_carousel_template_message()
        column1 = message.template.columns[0]
        removal_button = column1.actions[1]
        removal_postback_data = ProductRemovalPostbackDataModel.parse_raw(
            removal_button.data
        )

        self.assertEquals("remove", removal_postback_data.action)
        self.assertEquals("product_code1", removal_postback_data.product_code)
