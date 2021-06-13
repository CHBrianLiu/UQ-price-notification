from enum import Enum
from typing import List

from pydantic import BaseModel


class DatabaseTypeEnum(str, Enum):
    azure_blob = "AzureBlob"


class AppConfig(BaseModel):
    # APP
    TRACKING_ITEM_MAXIMUM: int

    # Debug mode
    LOCAL_TESTING: bool

    # LINE ENDPOINTS
    LINE_REPLY_ENDPOINT: str
    LINE_PUSH_ENDPOINT: str
    LINE_LINE_BOT_USER_ID: str
    LINE_LINE_BOT_CHANNEL_SECRET: str
    LINE_LINE_BOT_CHANNEL_TOKEN: str

    # OPERATION PATTERNS
    DELETE_REGEX_PATTERN: str
    DELETE_REGEX_PATTERN_PRODUCT_ID_GROUP_INDEX: int
    CONFIRM_ADDING_REGEX_PATTERN: str
    CONFIRM_ADDING_REGEX_PATTERN_PRODUCT_ID_GROUP_INDEX: int
    UQ_PRODUCT_URL_REGEX: str
    UQ_PRODUCT_URL_REGEX_PRODUCT_ID_GROUP_INDEX: int

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
    UQ_PRODUCT_CURRENCY: str

    # CRON
    CRON_PRICE_CHECKING: str
    CRON_NOTIFICATION_PUSHING: str
