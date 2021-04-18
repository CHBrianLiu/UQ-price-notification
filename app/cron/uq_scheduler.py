import asyncio
import logging
import time

import schedule
from app.config.loader import get_config_by_key
from app.cron import uq_job


@schedule.repeat(
    schedule.every().day.at(get_config_by_key("cron.price_checking"))
)
def check_pricing():
    logging.info("Start to check products prices.")
    asyncio.create_task(uq_job.check_pricing())


@schedule.repeat(
    schedule.every().day.at(get_config_by_key("cron.notification_pushing"))
)
def push_notification():
    logging.info("Start to push notification.")
    asyncio.create_task(uq_job.notify())


async def scheduler():
    logging.info("Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(600)
