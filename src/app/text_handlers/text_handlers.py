from linebot import models

from src.app.text_handlers.text_dispatcher import (
    ITextMessageHandler,
    TextMessageDispatcher,
)
from src.shared.line.message_creators.basic_message_creators import HelpMessageCreator

text_message_dispatcher = TextMessageDispatcher()


class TextMessageHandlerBase(ITextMessageHandler):
    _message: str
    _source_user_id: str

    def __init__(self, message: str, source_user_id: str):
        super(TextMessageHandlerBase, self).__init__(message, source_user_id)
        self._message = message
        self._source_user_id = source_user_id


@text_message_dispatcher.add_default
class DefaultTextMessageHandler(TextMessageHandlerBase):
    @staticmethod
    def is_command(message: str) -> bool:
        """
        This method doesn't matter when it's a default message handler.
        """
        return True

    def execute(self) -> models.Message:
        return HelpMessageCreator().generate()
