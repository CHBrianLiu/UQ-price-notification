from fastapi import APIRouter

router = APIRouter()


@router.get(
    path="/callback",
)
async def receive_line_webhook():
    return {}
