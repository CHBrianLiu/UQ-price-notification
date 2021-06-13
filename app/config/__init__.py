"""
Application configuration global object

Usage:
    from app.config import app_config
    app_config.<CONFIG>
"""

import json
import os

import dotenv

from .config_model import AppConfig

DEFAULT_ENV_PATH = os.path.join(os.path.dirname(__file__), "../../default.env")
LOCAL_ENV_PATH = os.path.join(os.path.dirname(__file__), "../../local.env")

loaded_config = {
    **dotenv.dotenv_values(DEFAULT_ENV_PATH),
    **dotenv.dotenv_values(LOCAL_ENV_PATH),
    **os.environ,
}

# USE THIS AS CONFIG OBJECT
app_config = AppConfig(**loaded_config)
