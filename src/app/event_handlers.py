from linebot.models import MessageEvent, TextMessage, PostbackEvent

from src.app.routes import webhook_handler
from src.shared.line.postback_action_models import ProductRemovalPostbackDataModel


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message_event(event: MessageEvent):
    content: str = event.message.text
    # check url validity.
    product_code = get_product_code_from_mobile_url(content) or get_product_code_from_desktop_url(content)
    if product_code:
        return
    # default response
    return


def get_product_code_from_mobile_url(url: str) -> str | None:
    # https://m.uniqlo.com/tw/product?pid=u0000000009993
    pass


def get_product_code_from_desktop_url(url: str) -> str | None:
    # https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode=u0000000009993
    pass


@webhook_handler.add(PostbackEvent)
def handle_postback_event(event: PostbackEvent):
    data: str = event.postback.data
