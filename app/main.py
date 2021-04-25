import logging
import threading

from fastapi import FastAPI

from app.config import app_config
from app.cron import uq_scheduler, callback_scheduler
from app.line import webhook
from app.utils import callback, logger
from app.models.setup import setup_azure_blob

app = FastAPI()

# setup logger
logger.set_global_logger_level()
logging.debug("TEST")

# setup_database
setup_azure_blob()

# start scheduler
threading.Thread(target=uq_scheduler.scheduler_entry).start()
# To avoid app service going to sleep.
if app_config.AZURE_APP_SERVICE_CALLBACK_ENABLED:
    logging.info("Callback mode enabled.")
    threading.Thread(target=callback_scheduler.scheduler).start()
    app.include_router(callback.router)

app.include_router(webhook.router)
