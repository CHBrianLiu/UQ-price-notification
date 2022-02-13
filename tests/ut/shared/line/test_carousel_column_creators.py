import unittest
from unittest import mock

from linebot import models

from src.shared.line.carousel_column_creators import UqProductManagementTemplateColumnCreator
from src.shared.line.postback_action_models import ProductRemovalPostbackDataModel


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

        self.assertEqual("product", column.title)

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

        self.assertEqual("原價：NT$ 200\n特價：NT$ 100", column.text)

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

        self.assertEqual(product.website_url, go_website_button.uri)

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

        self.assertEqual("remove", removal_postback_data.action)
        self.assertEqual("product_code", removal_postback_data.product_code)
