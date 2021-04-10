import re
from typing import Dict, Union

from app.config.loader import get_config_by_key
from app.line import data_models, reply

UQ_URL_PREFIX = get_config_by_key("uq.product_url_prefix")


async def handle_event(event: data_models.EventType) -> None:
    # Message event
    if event.get("type", "") == "message":
        handle_message_event(event)


async def handle_message_event(message_event: data_models.EventType):
    message_info = message_event.get("message", {})

    if message_info.get("type", "") == "text":
        handle_message_text_event(message_event)


async def handle_message_text_event(message_event: data_models.EventType):
    message_info = message_event.get("message", {})
    text_content = message_info.get("text", "")

    if text_content.upper().startswith("LIST") or text_content.startswith("清單"):
        # List all the client's tracked products.
        await reply.reply_list_message(message_event)
    elif text_content.upper().startswith("DELETE") or text_content.startswith("刪除"):
        # Delete one tracked product.
        await reply.reply_delete_message(message_event)
    elif text_content.startswith(UQ_URL_PREFIX):
        # Track this product.
        await reply.reply_add_message(message_event)
    else:
        # Show help message
        await reply.reply_help_message(message_event)
