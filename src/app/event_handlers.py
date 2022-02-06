import linebot
from linebot.models import MessageEvent, TextMessage, PostbackEvent

from src.shared.uq import uq_url_utils
from src.shared.line import plain_messages
from src import config

line_api = linebot.LineBotApi(config.LINE_CHANNEL_TOKEN, config.LINE_API_ENDPOINT)
webhook_handler = linebot.WebhookHandler(config.LINE_CHANNEL_SECRET)


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message_event(event: MessageEvent):
    content: str = event.message.text
    reply_token = event.reply_token
    # check url validity.
    product_code = uq_url_utils.UqProductCodeParser(content).get_product_code_from_url()
    if product_code:
        return
    # default response
    message = plain_messages.HelpMessageCreator().generate_help_message()
    line_api.reply_message(reply_token, message)

    return


@webhook_handler.add(PostbackEvent)
def handle_postback_event(event: PostbackEvent):
    data: str = event.postback.data
