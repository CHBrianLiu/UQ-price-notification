from enum import Enum
from typing import List

from pydantic import BaseModel


class DatabaseTypeEnum(str, Enum):
    azure_blob = "AzureBlob"


class AppConfig(BaseModel):
    # Debug mode
    LOCAL_TESTING: bool
    # LINE ENDPOINTS
    LINE_REPLY_ENDPOINT: str
    LINE_PUSH_ENDPOINT: str
    LINE_LINE_BOT_USER_ID: str
    LINE_LINE_BOT_CHANNEL_SECRET: str
    LINE_LINE_BOT_CHANNEL_TOKEN: str

    # DATABASE
    DATABASE_CLASS: DatabaseTypeEnum

    # LOGGING
    LOGGING_LEVEL: str

    # AZURE
    AZURE_ACCOUNT_NAME: str
    AZURE_ACCOUNT_KEY: str
    AZURE_APP_SERVICE_CALLBACK_ENABLED: bool  # Call itself to make app service awake
    AZURE_WEB_APP_CALLBACK_URL: str

    # UQ
    UQ_PRODUCT_URL_PREFIX: str
    UQ_PRODUCT_URL_REGEX: str

    # CRON
    CRON_PRICE_CHECKING: str
    CRON_NOTIFICATION_PUSHING: str
