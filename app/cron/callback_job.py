import logging

import requests
from app.config import app_config


def callback():
    logging.info(f"Call {app_config.AZURE_WEB_APP_CALLBACK_URL} to keep app awake.")
    with requests.get(app_config.AZURE_WEB_APP_CALLBACK_URL) as response:
        if not response.ok:
            logging.error("Call back error with code %s.", response.status_code)
