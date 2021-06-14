import re

from app.config import app_config
from app.line import data_models, reply
from app.line.actions import (
    add_tracking_product,
    confirm_product_adding,
    delete_tracking_product,
    list_tracking_products,
)


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

    list_operation_matcher = re.match(
        app_config.LIST_REGEX_PATTERN, text_content, re.IGNORECASE
    )
    uq_url_matcher = re.match(app_config.UQ_PRODUCT_URL_REGEX, text_content)
    confirm_operation_matcher = re.match(
        app_config.CONFIRM_ADDING_REGEX_PATTERN, text_content, re.IGNORECASE
    )
    delete_operation_matcher = re.match(
        app_config.DELETE_REGEX_PATTERN, text_content, re.IGNORECASE
    )

    if list_operation_matcher is not None:
        # List all the client's tracked products.
        response = await list_tracking_products(user_id)
        await reply.reply_list_message(message_event, response)
    elif delete_operation_matcher is not None:
        # Delete one tracked product.
        product_id = delete_operation_matcher.group(
            app_config.DELETE_REGEX_PATTERN_PRODUCT_ID_GROUP_INDEX
        )
        response = delete_tracking_product(user_id, product_id)
        await reply.reply_delete_message(message_event, response)
    elif confirm_operation_matcher is not None:
        # To add one product into the list.
        product_id = confirm_operation_matcher.group(
            app_config.CONFIRM_ADDING_REGEX_PATTERN_PRODUCT_ID_GROUP_INDEX
        )
        response = await add_tracking_product(user_id, product_id)
        await reply.reply_add_message(message_event, response)
    elif uq_url_matcher is not None:
        # UQ Product URL detected. Send confirm model
        product_id = uq_url_matcher.group(
            app_config.UQ_PRODUCT_URL_REGEX_PRODUCT_ID_GROUP_INDEX
        )
        response = await confirm_product_adding(product_id)
        await reply.reply_confirm_adding_message(message_event, response)
    else:
        # Show help message
        await reply.reply_help_message(message_event, text_content)
