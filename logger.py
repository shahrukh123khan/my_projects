"""
logger.py

Application logger.
Logs are written to both the console and logs/scraper.log.
"""

import logging
import sys

from config import LOG_FILE


def setup_logger():

    logger = logging.getLogger("ClutchScraper")

    # Prevent duplicate handlers if imported multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ----------------------------
    # Console Logger
    # ----------------------------
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # ----------------------------
    # File Logger
    # ----------------------------
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


logger = setup_logger()