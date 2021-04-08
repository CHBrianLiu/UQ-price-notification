import logging
from typing import Any, Dict, List, Optional, Union

from fastapi.exceptions import HTTPException

from app.config.loader import get_config_by_key
from fastapi import APIRouter, Header, Depends, Request
from linebot.models import Event, MessageEvent
from linebot.webhook import WebhookParser
from linebot.exceptions import InvalidSignatureError
from pydantic import BaseModel

router = APIRouter()
parser = WebhookParser(get_config_by_key("line.line_channel_secret"))


class LineRequest(BaseModel):
    destination: str
    events: List[Dict[str, Union[str, dict]]]


async def validate_signature(
    request: Request, x_line_signature: Optional[str] = Header(None)
):
    body = await request.body()
    if x_line_signature is None or not parser.signature_validator.validate(
        body.decode("utf-8"), x_line_signature
    ):
        logging.warning("Get request with faulty signature.")
        raise HTTPException(status_code=400, detail="Wrong signature")


@router.post(path="/line/webhook", dependencies=[Depends(validate_signature)])
async def receive_line_webhook(body: LineRequest):
    return {}
