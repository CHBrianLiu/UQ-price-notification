import linebot
from linebot.models import MessageEvent, TextMessage, PostbackEvent
import requests

from src.shared.uq import uq_url_utils, uq_product
from src.shared.line import plain_messages, product_subscription
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
        process_product_subscription_attempt(product_code, reply_token)
        return
    # default response
    message = plain_messages.HelpMessageCreator().generate_help_message()
    line_api.reply_message(reply_token, message)

    return


def process_product_subscription_attempt(product_code: str, reply_token: str):
    try:
        with requests.Session() as session:
            uq_retriever = uq_product.UqRetriever(product_code, session)
            product = uq_product.UqProduct(uq_retriever)
            creator = product_subscription.UqProductSubscriptionConfirmationMessageCreator(product)
            message = creator.generate_product_subscription_confirmation_message()

    except uq_product.UqProductException:
        message = plain_messages.ProductUrlErrorMessageCreator().generate_product_url_error_message()

    line_api.reply_message(reply_token, message)


@webhook_handler.add(PostbackEvent)
def handle_postback_event(event: PostbackEvent):
    data: str = event.postback.data
