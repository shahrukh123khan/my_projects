"""
utils.py

Common helper functions used throughout the project.
"""

import random
import time
from datetime import timedelta

from config import (
    MIN_SLEEP,
    MAX_SLEEP,
    LONG_BREAK_EVERY,
    LONG_BREAK_MIN,
    LONG_BREAK_MAX,
)

from logger import logger


# ============================================================
# Sleep Helpers
# ============================================================

def random_sleep(min_sleep=None, max_sleep=None):
    """
    Sleep for a random amount of time.

    Example:
        random_sleep()
        random_sleep(5, 10)
    """

    if min_sleep is None:
        min_sleep = MIN_SLEEP

    if max_sleep is None:
        max_sleep = MAX_SLEEP

    delay = random.uniform(min_sleep, max_sleep)

    logger.info(f"Sleeping for {delay:.2f} seconds")

    time.sleep(delay)


def long_break(page_number: int):
    """
    Give the browser a longer break every N pages.
    """

    if page_number == 0:
        return

    if page_number % LONG_BREAK_EVERY != 0:
        return

    delay = random.randint(
        LONG_BREAK_MIN,
        LONG_BREAK_MAX
    )

    logger.info(
        "=" * 70
    )

    logger.info(
        f"Taking long break ({delay} sec)"
    )

    logger.info(
        "=" * 70
    )

    time.sleep(delay)


# ============================================================
# Time Helpers
# ============================================================

def format_seconds(seconds: float) -> str:
    """
    Convert seconds to HH:MM:SS.
    """

    return str(
        timedelta(
            seconds=int(seconds)
        )
    )


def elapsed_time(start_time: float) -> str:
    """
    Returns elapsed time since start.
    """

    return format_seconds(
        time.time() - start_time
    )


# ============================================================
# ETA
# ============================================================

def calculate_eta(
    start_time: float,
    current_page: int,
    total_pages: int
):
    """
    Estimate remaining scraper time.
    """

    completed = current_page

    if completed == 0:
        return "Calculating..."

    elapsed = time.time() - start_time

    average = elapsed / completed

    remaining_pages = total_pages - completed

    eta = remaining_pages * average

    return format_seconds(eta)


# ============================================================
# Progress
# ============================================================

def print_progress(
    page,
    total_pages,
    profile_index,
    total_profiles,
    reviews,
    start_time
):
    """
    Pretty progress output.
    """

    logger.info("=" * 80)

    logger.info(
        f"Page            : {page}/{total_pages}"
    )

    logger.info(
        f"Profile         : {profile_index}/{total_profiles}"
    )

    logger.info(
        f"Reviews         : {reviews}"
    )

    logger.info(
        f"Elapsed         : {elapsed_time(start_time)}"
    )

    logger.info(
        f"ETA             : {calculate_eta(start_time, page, total_pages)}"
    )

    logger.info("=" * 80)


# ============================================================
# Retry Helper
# ============================================================

def retry(
    func,
    retries=3,
    delay=2,
    *args,
    **kwargs
):
    """
    Retry any function.

    Example:

        result = retry(
            scrape_profile,
            retries=3,
            delay=5,
            url=url
        )
    """

    last_exception = None

    for attempt in range(
        1,
        retries + 1
    ):

        try:

            logger.info(
                f"Attempt {attempt}/{retries}"
            )

            return func(
                *args,
                **kwargs
            )

        except Exception as e:

            last_exception = e

            logger.exception(e)

            if attempt < retries:

                time.sleep(delay)

    raise last_exception


# ============================================================
# Number Formatter
# ============================================================

def human_number(number: int):
    """
    Convert numbers into readable form.

    1000 -> 1.0K
    1500000 -> 1.5M
    """

    if number >= 1_000_000:

        return f"{number / 1_000_000:.1f}M"

    if number >= 1_000:

        return f"{number / 1000:.1f}K"

    return str(number)