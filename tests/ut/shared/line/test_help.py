import unittest

from src.shared.line.help import HelpMessageCreator


class TestHelpMessageCreator(unittest.TestCase):
    def test_help_message_should_contain_correct_message(self):
        creator = HelpMessageCreator()
        message = creator.generate_help_message()

        self.assertEquals("請傳送商品網址", message.text)
