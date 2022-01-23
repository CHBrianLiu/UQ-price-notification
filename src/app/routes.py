import fastapi

from src.app import api_validators

router = fastapi.APIRouter()


@router.post(
    "/webhook",
    dependencies=[
        fastapi.Depends(api_validators.line_webhook_request_signature_validator)
    ],
)
async def line_message_api_webhook_api():
    """
    Respond 200 OK for every request that passes the signature validation
    """
    return


@router.get("/ping")
async def health_check_api():
    """
    Respond "pong" for every single request. This API is to keep the app awake on Heroku.
    """
    return {"message": "pong"}
