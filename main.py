"""
main.py

Entry point for the Clutch scraper.
"""

from config import (
    START_PAGE,
    END_PAGE,
)

from logger import logger
from driver import Browser
from checkpoint import Checkpoint
from writer import Writer
from scraper import ClutchScraper


def main():

    logger.info("=" * 80)
    logger.info("Starting Clutch Scraper")
    logger.info("=" * 80)

    browser = None
    writer = None

    try:

        # ----------------------------------------
        # Initialize Components
        # ----------------------------------------

        browser = Browser()

        checkpoint = Checkpoint()

        writer = Writer()

        state = checkpoint.load()

        # Start from configured page if no checkpoint exists
        if (
            state["page"] < START_PAGE
            or state["page"] > END_PAGE
        ):
            state["page"] = START_PAGE
            state["profile_index"] = 0
            checkpoint.save(state)

        scraper = ClutchScraper(
            browser=browser,
            writer=writer,
            checkpoint=checkpoint,
            state=state,
        )

        # ----------------------------------------
        # Start Scraping
        # ----------------------------------------

        scraper.run(END_PAGE)

        logger.info("=" * 80)
        logger.info("Scraping Finished Successfully")
        logger.info("=" * 80)

    except KeyboardInterrupt:

        logger.warning("Scraper stopped by user.")

    except Exception as e:

        logger.exception(e)

    finally:

        if writer:
            writer.close()

        if browser:
            browser.close()

        logger.info("Resources closed.")


if __name__ == "__main__":

    main()