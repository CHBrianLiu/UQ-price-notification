import unittest

from src.shared.line.message_creators.basic_message_creators import (
    HelpMessageCreator,
    PriceDownNotificationMessageCreator,
    ProductSuccessfullyAddedMessageCreator,
    ProductAlreadyInListMessageCreator
)


class TestHelpMessageCreator(unittest.TestCase):
    def test_help_message_should_contain_correct_message(self):
        creator = HelpMessageCreator()
        message = creator.generate()

        self.assertEqual("請傳送商品網址", message.text)


class TestPriceDownNotificationMessageCreator(unittest.TestCase):
    def test_price_down_notification_message_should_contain_correct_message(self):
        creator = PriceDownNotificationMessageCreator()
        message = creator.generate()

        self.assertEqual("你好，你追蹤的商品正在特價中！把握機會購買吧！", message.text)


class TestProductSuccessfullyAddedMessageCreator(unittest.TestCase):
    def test_product_successfully_added_message_should_contain_correct_message(self):
        product_name = "product_name"
        creator = ProductSuccessfullyAddedMessageCreator(product_name)
        message = creator.generate()

        self.assertEqual("已成功將product_name加入追蹤清單！", message.text)


class TestProductAlreadyInListMessageCreator(unittest.TestCase):
    def test_product_already_in_list_message_should_contain_correct_message(self):
        product_name = "product_name"
        creator = ProductAlreadyInListMessageCreator(product_name)
        message = creator.generate()

        self.assertEqual("product_name已經在你的追蹤清單了喔！", message.text)
