import logging
import threading

from fastapi import FastAPI

from app.config import app_config
from app.cron import callback_scheduler, uq_scheduler
from app.line import webhook
from app.line.rich_menu import prepare_rich_menu
from app.utils import callback, logger

app = FastAPI()

# setup logger
logger.set_global_logger_level()

# Setup LINE rich menu
prepare_rich_menu.setup()

# start scheduler
threading.Thread(target=uq_scheduler.scheduler).start()
# To avoid app service going to sleep.
if app_config.AZURE_APP_SERVICE_CALLBACK_ENABLED:
    app.include_router(callback.router)

app.include_router(webhook.router)
