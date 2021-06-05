import asyncio

from fastapi import APIRouter, Depends

from app.line import data_models, validator
from app.line.event_handlers import handle_event

router = APIRouter()


@router.post(
    path="/line/webhook",
    dependencies=[
        Depends(validator.validate_signature),
        # ? disable destination validation due to destination value spec unclear.
        # Depends(validator.validate_destination),
    ],
)
async def receive_line_webhook(body: data_models.LineRequest):
    for event in body.events:
        asyncio.create_task(handle_event(event))
    return {}
