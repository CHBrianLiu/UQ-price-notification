from typing import List
from pydantic import BaseModel


class AppConfig(BaseModel):
    # Debug mode
    LOCAL_TESTING: bool
    # LINE ENDPOINTS
    LINE_REPLY_ENDPOINT: str
    LINE_PUSH_ENDPOINT: str
    LINE_LINE_BOT_USER_ID: str
    LINE_LINE_BOT_CHANNEL_SECRET: str
    LINE_LINE_BOT_CHANNEL_TOKEN: str

    # LOGGING
    LOGGING_LEVEL: str

    # AZURE
    AZURE_BLOB_CONTAINERS: List[str]
    AZURE_ACCOUNT_NAME: str
    AZURE_ACCOUNT_KEY: str

    # UQ
    UQ_PRODUCT_URL_PREFIX: str
    UQ_PRODUCT_NAME_CSS: str
    UQ_ICON_LIST_CSS: str
    UQ_ON_SALE_ICON_CSS_LIST: List[str]
    UQ_HIDE_ICON_STYLE: str

    # CRON
    CRON_PRICE_CHECKING: str
    CRON_NOTIFICATION_PUSHING: str
