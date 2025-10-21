"""
Setup API logger.
"""

import logging

from src.config import config

DOT_API_LOGGER_NAME = "DOT API"


def get_dot_api_logger():
    return logging.getLogger(DOT_API_LOGGER_NAME)


def configure_dot_api_logger():
    logger = get_dot_api_logger()

    if config.APP_ENV == "local" or config.APP_ENV == "dev":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s:%(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
