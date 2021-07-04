import re

from app.config import app_config
from app.line import data_models, reply
from app.line.actions import confirm_product_adding, list_tracking_products
from app.line.postback_handler import PostbackHandlerFactory


async def handle_event(event: data_models.EventType) -> None:
    # Message event
    if event.get("type", "") == "message":
        await handle_message_event(event)
    # Postback event
    elif event.get("type", "") == "postback":
        await handle_postback_event(data_models.PostbackEvent.parse_obj(event))


async def handle_message_event(message_event: data_models.EventType):
    message_info = message_event.get("message", {})

    if message_info.get("type", "") == "text":
        await handle_message_text_event(message_event)


async def handle_postback_event(postback_event: data_models.PostbackEvent):
    handler = PostbackHandlerFactory.create(
        postback_event.postback.data,
        postback_event.replyToken,
        postback_event.source,
    )
    handler.manipulate()
    await handler.reply_operation_result()


async def handle_message_text_event(message_event: data_models.EventType):
    message_info = message_event.get("message", {})
    text_content = message_info.get("text", "")
    user_id = message_event.get("source", {}).get("userId", "anonymous")

    list_operation_matcher = re.match(
        app_config.LIST_REGEX_PATTERN, text_content, re.IGNORECASE
    )
    uq_url_matcher = re.match(app_config.UQ_PRODUCT_URL_REGEX, text_content)

    if list_operation_matcher is not None:
        # List all the client's tracked products.
        response = await list_tracking_products(user_id)
        await reply.reply_list_message(message_event, response)
    elif uq_url_matcher is not None:
        # UQ Product URL detected. Send confirm model
        product_id = uq_url_matcher.group(
            app_config.UQ_PRODUCT_URL_REGEX_PRODUCT_ID_GROUP_INDEX
        )
        response = await confirm_product_adding(product_id)
        await reply.reply_adding_confirmation_message(message_event, response)
    else:
        # Show help message
        await reply.reply_help_message(message_event, text_content)
