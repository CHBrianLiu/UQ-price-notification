import base64
import hashlib
import hmac
import logging
from typing import Optional

from app.config.loader import get_config_by_key
from app.line import data_models
from fastapi import Header, Request
from fastapi.exceptions import HTTPException


async def validate_signature(
    request: Request, x_line_signature: Optional[str] = Header(None)
):
    body = await request.body()
    channel_secret = get_config_by_key("line.line_channel_secret")
    signature = base64.b64encode(
        hmac.new(channel_secret.encode("utf-8"), body, hashlib.sha256).digest()
    ).decode("utf-8")

    logging.debug(
        "computed signature: %s. received signature: %s", signature, x_line_signature
    )

    if x_line_signature is None or signature != x_line_signature:
        logging.warning("Get request with faulty signature.")
        raise HTTPException(status_code=400, detail="Wrong signature")


async def validate_destination(body: data_models.LineRequest):
    bot_user_id = get_config_by_key("line.line_bot_user_id")
    logging.debug(
        "bot_user_id: %s. Request body destination: %s", bot_user_id, body.destination
    )
    if body.destination is not None and body.destination != bot_user_id:
        raise HTTPException(status_code=400, detail="Wrong destination")
