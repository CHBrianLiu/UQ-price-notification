import linebot
from linebot.models import MessageEvent, TextMessage, PostbackEvent
import requests

from src.shared.line.message_creators import (
    HelpMessageCreator,
    LineMessageCreator,
    UqProductSubscriptionConfirmationMessageCreator,
    ProductUrlErrorMessageCreator,
)
from src import config
from src.shared.uq.uq_url_utils import UqProductCodeParser
from src.shared.uq import uq_product

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
def handle_postback_event(event: PostbackEvent):  # pylint: disable=W0613
    # TODO: Postback event handling logic  pylint: disable=W0511
    pass
