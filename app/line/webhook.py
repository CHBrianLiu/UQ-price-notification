from app.line import data_models, validator
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
    return {}
