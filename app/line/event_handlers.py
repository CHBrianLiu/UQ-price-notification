import re

from app.config import app_config
from app.line import data_models, reply
from app.line.actions import add_tracking_product, list_tracking_products


async def handle_event(event: data_models.EventType) -> None:
    # Message event
    if event.get("type", "") == "message":
        await handle_message_event(event)


async def handle_message_event(message_event: data_models.EventType):
    message_info = message_event.get("message", {})

    if message_info.get("type", "") == "text":
        await handle_message_text_event(message_event)


async def handle_message_text_event(message_event: data_models.EventType):
    message_info = message_event.get("message", {})
    text_content = message_info.get("text", "")
    user_id = message_event.get("source", {}).get("userId", "anonymous")
    uq_url_matcher = re.match(app_config.UQ_PRODUCT_URL_REGEX, text_content)

    if text_content.upper().startswith("LIST") or text_content.startswith("清單"):
        # List all the client's tracked products.
        response = list_tracking_products(user_id)
        await reply.reply_list_message(message_event, response)
    elif text_content.upper().startswith("DELETE") or text_content.startswith("刪除"):
        # Delete one tracked product.
        await reply.reply_delete_message(message_event)
    elif uq_url_matcher is not None:
        # Track this product.
        product_id = uq_url_matcher.group(1)
        response = await add_tracking_product(user_id, product_id)
        await reply.reply_add_message(message_event, response)
    else:
        # Show help message
        await reply.reply_help_message(message_event)
