import json
import logging
from typing import Any, Dict, List

import aiohttp
from app.config.loader import get_config_by_key
from app.line import data_models


async def reply(
    reply_token: str,
    messages: List[Dict[str, Any]],
    notification_disabled: bool = False,
):
    token = get_config_by_key("line.line_channel_token")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    body = json.dumps(
        {
            "replyToken": reply_token,
            "messages": messages,
            "notificationDisabled": notification_disabled,
        }
    )

    endpoint = get_config_by_key("line.reply_endpoint")
    async with aiohttp.ClientSession() as session:
        async with session.post(url=endpoint, data=body, headers=headers) as response:
            if response.status != 200:
                json_body = await response.json()
                logging.error(
                    "Failed to reply message. Code: %s, Response: %s",
                    response.status,
                    json_body,
                )


async def reply_list_message(event: data_models.EventType):
    await reply(event.get("replyToken", ""), [{"type": "text", "text": "目前你追蹤的商品："}])

async def reply_delete_message(event: data_models.EventType):
    await reply(event.get("replyToken", ""), [{"type": "text", "text": "取消追蹤商品："}])

async def reply_add_message(event: data_models.EventType):
    await reply(event.get("replyToken", ""), [{"type": "text", "text": "開始追蹤商品："}])

async def reply_help_message(event: data_models.EventType):
    await reply(event.get("replyToken", ""), [{"type": "text", "text": "可用指令："}])

