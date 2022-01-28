import base64
import hashlib
import hmac

import fastapi
from fastapi import exceptions

from src import config


def line_webhook_request_signature_validator(
    body: str = fastapi.Body(...), x_line_signature: str = fastapi.Header(...)
):
    if not is_webhook_signature_valid(
        body, config.LINE_CHANNEL_SECRET, x_line_signature
    ):
        raise exceptions.HTTPException(
            status_code=400, detail="Signature validation failed."
        )


def is_webhook_signature_valid(req_body: str, secret: str, header_signature: str):
    secret_in_bytes = secret.encode("utf-8")
    req_body_in_bytes = req_body.encode("utf-8")
    req_hash = hmac.new(secret_in_bytes, req_body_in_bytes, hashlib.sha256).digest()
    signature = base64.b64encode(req_hash).decode("utf-8")
    if signature != header_signature:
        return False
    return True
