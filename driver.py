"""
driver.py

Browser manager for the Clutch scraper.
"""

import time
from pathlib import Path

import undetected_chromedriver as uc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config import (
    HEADLESS,
    CHROME_VERSION,
    PAGE_LOAD_TIMEOUT,
    ELEMENT_TIMEOUT,
    MAX_PAGE_RETRIES,
    SCREENSHOT_DIR,
)

from logger import logger


class Browser:

    def __init__(self):

        self.driver = None
        self.wait = None

        self.start()

    # ======================================================
    # Start Browser
    # ======================================================

    def start(self):

        logger.info("Starting Chrome browser...")

        # options = uc.ChromeOptions()

        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--start-maximized")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--no-sandbox")
        options = uc.ChromeOptions()

        prefs = {
            "profile.managed_default_content_settings.images": 2
        }

        options.add_experimental_option(
            "prefs",
            prefs
        )

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        
        self.driver = uc.Chrome(
            version_main=CHROME_VERSION,
            options=options,
            headless=HEADLESS,
        )

        self.driver.set_page_load_timeout(
            PAGE_LOAD_TIMEOUT
        )

        self.wait = WebDriverWait(
            self.driver,
            ELEMENT_TIMEOUT
        )

        logger.info("Chrome started successfully.")

    # ======================================================
    # Open URL
    # ======================================================

    def safe_get(
        self,
        url,
        retries=MAX_PAGE_RETRIES,
    ):

        for attempt in range(1, retries + 1):

            try:

                logger.info(
                    f"Opening URL ({attempt}/{retries})"
                )

                self.driver.get(url)

                return True

            except TimeoutException:

                logger.warning(
                    "Page load timeout."
                )

            except Exception as e:

                logger.exception(e)

            time.sleep(3)

        logger.error(
            f"Unable to load:\n{url}"
        )

        return False

    # ======================================================
    # Restart Browser
    # ======================================================

    def restart(self):

        logger.info("=" * 80)
        logger.info("Restarting browser...")
        logger.info("=" * 80)

        try:
            self.driver.quit()
        except Exception:
            pass

        time.sleep(5)

        self.start()

    # ======================================================
    # Screenshot
    # ======================================================

    def screenshot(
        self,
        name
    ):

        try:

            filename = Path(
                SCREENSHOT_DIR
            ) / f"{name}.png"

            self.driver.save_screenshot(
                str(filename)
            )

            logger.info(
                f"Screenshot saved: {filename}"
            )

        except Exception as e:

            logger.exception(e)

    # ======================================================
    # Close Browser
    # ======================================================

    def close(self):

        try:

            logger.info("Closing browser...")

            self.driver.quit()

        except Exception:

            pass