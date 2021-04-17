import logging

from fastapi import FastAPI

from app.config.loader import get_config_by_key
from app.line import webhook
from app.models.setup import setup_azure_blob

app = FastAPI()
logger = logging.getLogger()

log_level = get_config_by_key("logging.level")
if log_level == "critical":
    logger.setLevel(logging.CRITICAL)
elif log_level == "warning":
    logger.setLevel(logging.WARNING)
elif log_level == "info":
    logger.setLevel(logging.INFO)
elif log_level == "debug":
    logger.setLevel(logging.DEBUG)
else:
    # Default is error
    logger.setLevel(logging.ERROR)
    
# setup_database
setup_azure_blob()

app.include_router(webhook.router)
