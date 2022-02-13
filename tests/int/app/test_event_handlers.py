import unittest
from unittest import mock

import linebot
from linebot.models import (
    MessageEvent,
    TextMessage,
    TemplateSendMessage,
    ButtonsTemplate,
)

from src.app.event_handlers import handle_text_message_event
from src.shared.uq import uq_product


class TestTextMessageEventHandler(unittest.TestCase):
    def test_reply_general_message_to_nonsense_text_message(self):
        # we need to mock the reply_message method because we want to test the method call
        with mock.patch.object(
            linebot.LineBotApi, "reply_message"
        ) as reply_message_method:
            coming_message = TextMessage(text="nonsense message")
            message_event = MessageEvent(
                message=coming_message, reply_token="reply_token"
            )

            handle_text_message_event(message_event)

            reply_message_method.assert_called_with(
                "reply_token", TextMessage(text="請傳送商品網址")
            )

    def test_reply_product_subscription_confirmation_message_to_correct_product_desktop_url(
        self,
    ):
        # we need to mock the reply_message method because we want to test the method call
        with mock.patch.object(
            linebot.LineBotApi, "reply_message"
        ) as reply_message_method:
            coming_message = TextMessage(
                text="https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode=u0000000009993"
            )
            message_event = MessageEvent(
                message=coming_message, reply_token="reply_token"
            )

            handle_text_message_event(message_event)

            reply_message_method.assert_called_once()
            self.assertEqual(reply_message_method.call_args.args[0], "reply_token")
            actual_reply_message = reply_message_method.call_args.args[1]
            self.assertIsInstance(actual_reply_message, TemplateSendMessage)
            self.assertIsInstance(actual_reply_message.template, ButtonsTemplate)
            # We don't test the body of the reply message because it contains the price that is
            # the subject to change in relatively high frequency.
            self.assertEqual(actual_reply_message.template.title, "男裝 V領T恤(短袖) 433026")

    def test_reply_product_subscription_confirmation_message_to_correct_product_mobile_url(
        self,
    ):
        # we need to mock the reply_message method because we want to test the method call
        with mock.patch.object(
            linebot.LineBotApi, "reply_message"
        ) as reply_message_method:
            coming_message = TextMessage(
                text="https://m.uniqlo.com/tw/product?pid=u0000000009993"
            )
            message_event = MessageEvent(
                message=coming_message, reply_token="reply_token"
            )

            handle_text_message_event(message_event)

            reply_message_method.assert_called_once()
            self.assertEqual(reply_message_method.call_args.args[0], "reply_token")
            actual_reply_message = reply_message_method.call_args.args[1]
            self.assertIsInstance(actual_reply_message, TemplateSendMessage)
            self.assertIsInstance(actual_reply_message.template, ButtonsTemplate)
            # We don't test the body of the reply message because it contains the price that is
            # the subject to change in relatively high frequency.
            self.assertEqual(actual_reply_message.template.title, "男裝 V領T恤(短袖) 433026")

    def test_reply_invlid_product_code_message_to_wrong_product_url(self):
        # we need to mock the reply_message method because we want to test the method call
        with mock.patch.object(
            linebot.LineBotApi, "reply_message"
        ) as reply_message_method:
            coming_message = TextMessage(
                text="https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode=nonexisting"
            )
            message_event = MessageEvent(
                message=coming_message, reply_token="reply_token"
            )

            handle_text_message_event(message_event)

            reply_message_method.assert_called_with(
                "reply_token", TextMessage(text="你所輸入的商品網址有誤，請重新輸入！")
            )
