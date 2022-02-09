import linebot
from linebot.models import MessageEvent, TextMessage, PostbackEvent

from src.shared.line.message_creators import HelpMessageCreator
from src import config

line_api = linebot.LineBotApi(config.LINE_CHANNEL_TOKEN, config.LINE_API_ENDPOINT)
webhook_handler = linebot.WebhookHandler(config.LINE_CHANNEL_SECRET)


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message_event(event: MessageEvent):
    reply_token = event.reply_token

    # default response
    message = HelpMessageCreator().generate()
    line_api.reply_message(reply_token, message)


@webhook_handler.add(PostbackEvent)
def handle_postback_event(event: PostbackEvent):  # pylint: disable=W0613
    # TODO: Postback event handling logic  pylint: disable=W0511
    pass
