import asyncio
import logging
import time

import schedule

from app.config import app_config
from app.cron import uq_job


@schedule.repeat(schedule.every().day.at(app_config.CRON_PRICE_CHECKING))
def check_pricing():
    logging.info("Start to check products prices.")
    asyncio.run(uq_job.check_pricing())


@schedule.repeat(schedule.every().day.at(app_config.CRON_NOTIFICATION_PUSHING))
def push_notification():
    logging.info("Start to push notification.")
    asyncio.run(uq_job.notify())

def scheduler():
    logging.info("Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(1)
