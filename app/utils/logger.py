import logging

from app.config import app_config


def set_global_logger_level():
    logger = logging.getLogger()

    log_level = app_config.LOGGING_LEVEL
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
