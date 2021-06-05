import logging
import schedule

from app.cron import callback_job
from app.config import app_config


@schedule.repeat(schedule.every().minutes)
def do_callback():
    if app_config.AZURE_APP_SERVICE_CALLBACK_ENABLED:
        logging.info("Keep awake.")
        callback_job.callback()
