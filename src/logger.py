"""
Setup API logger.
"""

import logging

DOT_API_LOGGER_NAME = "DOT API"


def get_dot_api_logger():
    return logging.getLogger(DOT_API_LOGGER_NAME)


def configure_dot_api_logger():
    logger = get_dot_api_logger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s:%(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
