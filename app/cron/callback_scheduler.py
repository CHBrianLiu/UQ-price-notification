import asyncio
import logging
import schedule
import time

from app.cron import callback_job


@schedule.repeat(schedule.every().minutes)
def do_callback():
    logging.info("Keep awake.")
    callback_job.callback()


def scheduler():
    logging.info("Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(30)
