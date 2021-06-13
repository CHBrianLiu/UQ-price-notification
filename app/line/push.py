import json
import logging
from typing import Any, Dict, List

import aiohttp

from app.config import app_config
from app.line.messages import TextMessage
from app.line.push_messages import price_down_messages
from app.line.utils import compose_product_carousel


async def push(
    to_id: str,
    messages: List[Dict[str, Any]],
    notification_disabled: bool = False,
):
    token = app_config.LINE_LINE_BOT_CHANNEL_TOKEN
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    body = json.dumps(
        {
            "to": to_id,
            "messages": messages,
            "notificationDisabled": notification_disabled,
        }
    )

    endpoint = app_config.LINE_PUSH_ENDPOINT
    async with aiohttp.ClientSession() as session:
        async with session.post(url=endpoint, data=body, headers=headers) as response:
            if response.status != 200:
                json_body = await response.json()
                logging.error(
                    "Failed to push message. Code: %s, Response: %s",
                    response.status,
                    json_body,
                )


async def push_price_down_message(user_id: str, product_ids: List[str]):
    headline = TextMessage(text=price_down_messages.messages.get("headline"))
    products = await compose_product_carousel(product_ids)
    await push(
        user_id,
        [
            headline.dict(exclude_none=True),
            products.dict(exclude_none=True),
        ],
    )
