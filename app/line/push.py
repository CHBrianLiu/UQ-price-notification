import json
import logging
from typing import Any, Dict, List, Tuple

import aiohttp
from app.config.loader import get_config_by_key
from app.line import data_models
from app.line.push_messages import price_down_messages


async def push(
    to_id: str,
    messages: List[Dict[str, Any]],
    notification_disabled: bool = False,
):
    token = get_config_by_key("line.line_channel_token")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    body = json.dumps(
        {
            "to": to_id,
            "messages": messages,
            "notificationDisabled": notification_disabled,
        }
    )

    endpoint = get_config_by_key("line.push_endpoint")
    async with aiohttp.ClientSession() as session:
        async with session.post(url=endpoint, data=body, headers=headers) as response:
            if response.status != 200:
                json_body = await response.json()
                logging.error(
                    "Failed to push message. Code: %s, Response: %s",
                    response.status,
                    json_body,
                )


async def push_price_down_message(
    user_id: str, response: Tuple[str, Dict[str, Any]]
):
    message = price_down_messages.messages[response[0]].format(**(response[1]))
    await push(user_id, [{"type": "text", "text": message}])
