import asyncio

from app.line import data_models, validator
from app.line.event_handlers import handle_event
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post(
    path="/line/webhook",
    dependencies=[
        Depends(validator.validate_signature),
        Depends(validator.validate_destination),
    ],
)
async def receive_line_webhook(body: data_models.LineRequest):
    for event in body.events:
        asyncio.create_task(handle_event(event))
    return {}
