import linebot
from linebot.models import MessageEvent, TextMessage, PostbackEvent

from src import config

line_api = linebot.LineBotApi(config.LINE_CHANNEL_TOKEN, config.LINE_API_ENDPOINT)
webhook_handler = linebot.WebhookHandler(config.LINE_CHANNEL_SECRET)


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message_event(event: MessageEvent):
    # TODO: Text message event handling logics
    pass


@webhook_handler.add(PostbackEvent)
def handle_postback_event(event: PostbackEvent):
    # TODO: Postback event handling logic
    pass
