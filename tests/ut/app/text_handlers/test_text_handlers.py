import unittest

from linebot import models

from src.app.text_handlers.text_handlers import DefaultTextMessageHandler


class TestDefaultTextMessageHandler(unittest.TestCase):
    def test_execute_should_generate_help_message(self):
        handler = DefaultTextMessageHandler("any message", "user_id")

        response_message = handler.execute()

        self.assertIsInstance(response_message, models.Message)
        self.assertEqual(response_message.text, "請傳送商品網址")
