import unittest
from unittest import mock

from linebot import models

from src.shared.line.postback_action_models import ProductRemovalPostbackDataModel
from src.shared.line.product_management import (
    UqProductManagementTemplateMessageCreator,
    UqProductManagementTemplateColumnCreator,
)


class TestUqProductManagementTemplateColumnCreator(unittest.TestCase):
    def test_products_carousel_template_column_title_should_be_product_name(self):
        product = mock.MagicMock()
        product.name = "product"
        product.product_code = "product_code"
        product.website_url = "https://abcd.com/product"
        product.is_on_sale = False
        product.original_price = 200

        creator = UqProductManagementTemplateColumnCreator(product)
        column = creator.generate_product_carousel_column()

        self.assertEquals("product", column.title)

    def test_products_carousel_template_column_content_should_use_corrent_format_if_product_is_on_sale(
        self,
    ):
        product = mock.MagicMock()
        product.name = "product"
        product.product_code = "product_code"
        product.website_url = "https://abcd.com/product"
        product.is_on_sale = True
        product.original_price = 200
        product.special_offer = 100

        creator = UqProductManagementTemplateColumnCreator(product)
        column = creator.generate_product_carousel_column()

        self.assertEquals("原價：NT$ 200\n特價：NT$ 100", column.text)

    def test_products_carousel_template_column_should_contain_go_website_and_removal_actions(
        self,
    ):
        product = mock.MagicMock()
        product.name = "product"
        product.product_code = "product_code"
        product.website_url = "https://abcd.com/product1"
        product.special_offer = 100

        creator = UqProductManagementTemplateColumnCreator(product)
        column = creator.generate_product_carousel_column()
        go_website_button = column.actions[0]
        removal_button = column.actions[1]

        self.assertIsInstance(go_website_button, models.URIAction)
        self.assertIsInstance(removal_button, models.PostbackAction)

    def test_products_carousel_template_column_go_website_button_link_should_be_product_website(
        self,
    ):
        product = mock.MagicMock()
        product.name = "product"
        product.product_code = "product_code"
        product.website_url = "https://abcd.com/product1"
        product.special_offer = 100

        creator = UqProductManagementTemplateColumnCreator(product)
        column = creator.generate_product_carousel_column()
        go_website_button = column.actions[0]

        self.assertEquals(product.website_url, go_website_button.uri)

    def test_products_carousel_template_column_removal_button_link_should_contain_correct_data(
        self,
    ):
        product = mock.MagicMock()
        product.name = "product"
        product.product_code = "product_code"
        product.website_url = "https://abcd.com/product"
        product.special_offer = 100

        creator = UqProductManagementTemplateColumnCreator(product)
        column = creator.generate_product_carousel_column()
        removal_button = column.actions[1]
        removal_postback_data = ProductRemovalPostbackDataModel.parse_raw(
            removal_button.data
        )

        self.assertEquals("remove", removal_postback_data.action)
        self.assertEquals("product_code", removal_postback_data.product_code)


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
        message = creator.generate_products_carousel_template_message()
        column1 = message.template.columns[0]
        column2 = message.template.columns[1]

        self.assertEquals(2, len(message.template.columns))
        self.assertEquals("product1", column1.title)
        self.assertEquals("product2", column2.title)
