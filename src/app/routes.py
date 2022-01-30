import fastapi
import linebot
import linebot.exceptions

from src import config

router = fastapi.APIRouter()
webhook_handler = linebot.WebhookHandler(config.LINE_CHANNEL_SECRET)


@router.post("/webhook")
async def line_message_api_webhook_api(body: str = fastapi.Body(...), x_line_signature: str = fastapi.Header(...)):
    """
    Respond 200 OK for every request that passes the signature validation
    """
    try:
        webhook_handler.handle(body, x_line_signature)
    except linebot.exceptions.InvalidSignatureError as e:
        raise fastapi.HTTPException(400) from e
    return


@router.get("/ping")
async def health_check_api():
    """
    Respond "pong" for every single request. This API is to keep the app awake on Heroku.
    """
    return {"message": "pong"}
