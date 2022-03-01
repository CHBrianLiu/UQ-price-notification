import linebot
from linebot.models import MessageEvent, TextMessage, PostbackEvent
import requests

from src.shared.line.message_creators.base_creators import LineMessageCreator
from src.shared.line.message_creators.template_message_creators import (
    UqProductSubscriptionConfirmationMessageCreator,
)
from src.shared.line.message_creators.basic_message_creators import (
    HelpMessageCreator,
    ProductUrlErrorMessageCreator,
)
from src import config
from src.shared.uq.uq_url_utils import UqProductCodeParser
from src.shared.uq import uq_product
from src.app.postback_handlers import postback_dispatcher

line_api = linebot.LineBotApi(config.LINE_CHANNEL_TOKEN, config.LINE_API_ENDPOINT)
webhook_handler = linebot.WebhookHandler(config.LINE_CHANNEL_SECRET)


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message_event(event: MessageEvent):
    reply_token = event.reply_token
    message = event.message.text

    if product_code := UqProductCodeParser(message).get_product_code_from_url():
        reply_message = generate_response_for_given_product_code(product_code)
    else:
        reply_message = HelpMessageCreator().generate()

    line_api.reply_message(reply_token, reply_message)


def generate_response_for_given_product_code(product_code: str) -> LineMessageCreator:
    try:
        with requests.Session() as session:
            retriever = uq_product.UqRetriever(product_code, session)
            product = uq_product.UqProduct(retriever)
            message = UqProductSubscriptionConfirmationMessageCreator(
                product
            ).generate()

    except uq_product.UqProductException:
        message = ProductUrlErrorMessageCreator().generate()

    return message


@webhook_handler.add(PostbackEvent)
def handle_postback_event(event: PostbackEvent):
    # Currently, only normal users can interact with our bot.
    if event.source.type != "user":
        return
    response = postback_dispatcher.run_task(event.postback.data, event.source.user_id)
    line_api.reply_message(event.reply_token, response)
