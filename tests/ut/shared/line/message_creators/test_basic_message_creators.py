import unittest

from src.shared.line.message_creators.basic_message_creators import (
    HelpMessageCreator,
    PriceDownNotificationMessageCreator,
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
