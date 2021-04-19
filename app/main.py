import asyncio
import logging
import asyncio
import threading

from fastapi import FastAPI

from app.config.loader import get_config_by_key
from app.line import webhook
from app.models.setup import setup_azure_blob
from app.cron import uq_scheduler

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

# start scheduler
# if asyncio.get_event_loop() is None:
#     scheduler_event_loop = asyncio.new_event_loop().run_until_complete(uq_scheduler.scheduler())
# else:
#     asyncio.create_task(uq_scheduler.scheduler())
threading.Thread(target=uq_scheduler.scheduler_entry).start()

app.include_router(webhook.router)
