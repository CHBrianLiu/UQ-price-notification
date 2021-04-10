import json
import logging
from typing import Any, Dict, List

import aiohttp
from app.config.loader import get_config_by_key


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
