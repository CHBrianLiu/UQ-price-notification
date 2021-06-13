import json
import logging
from typing import Any, Dict, List, Tuple

import aiohttp

from app.config import app_config
from app.line import data_models
from app.line.messages import TextMessage
from app.line.reply_messages import (
    ResponseMessageType,
    add_messages,
    delete_messages,
    help_messages,
    list_messages,
    confirm_add_messages,
)


async def reply(
    reply_token: str,
    messages: List[Dict[str, Any]],
    notification_disabled: bool = False,
):
    token = app_config.LINE_LINE_BOT_CHANNEL_TOKEN
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    body = json.dumps(
        {
            "replyToken": reply_token,
            "messages": messages,
            "notificationDisabled": notification_disabled,
        }
    )

    endpoint = app_config.LINE_REPLY_ENDPOINT
    async with aiohttp.ClientSession() as session:
        async with session.post(url=endpoint, data=body, headers=headers) as response:
            if response.status != 200:
                json_body = await response.json()
                logging.error(
                    "Failed to reply message. Code: %s, Response: %s",
                    response.status,
                    json_body,
                )


async def reply_list_message(
    event: data_models.EventType, response: ResponseMessageType
):
    if response[0] in list_messages.messages.keys():
        message = TextMessage(
            text=list_messages.messages[response[0]].format(**(response[1]))
        ).dict(exclude_none=True)
    else:
        message = response[1]
    await reply(event.get("replyToken", ""), [message])


async def reply_delete_message(
    event: data_models.EventType, response: ResponseMessageType
):
    message = delete_messages.messages[response[0]].format(**(response[1]))
    await reply(event.get("replyToken", ""), [{"type": "text", "text": message}])


async def reply_add_message(
    event: data_models.EventType, response: ResponseMessageType
):
    message = add_messages.messages[response[0]].format(**(response[1]))
    await reply(event.get("replyToken", ""), [{"type": "text", "text": message}])


async def reply_confirm_adding_message(
    event: data_models.EventType, response: ResponseMessageType
):
    if response[0] in confirm_add_messages.messages.keys():
        message = TextMessage(
            text=confirm_add_messages.messages[response[0]].format(**(response[1]))
        ).dict(exclude_none=True)
    else:
        message = response[1]
    await reply(event.get("replyToken", ""), [message])


async def reply_help_message(event: data_models.EventType, keyword: str):
    text = (
        help_messages.messages.get(keyword)
        if keyword in help_messages.messages
        else help_messages.messages["help"]
    )
    await reply(
        event.get("replyToken", ""),
        [{"type": "text", "text": text}],
    )
