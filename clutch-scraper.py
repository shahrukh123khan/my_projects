"""
scraper.py

Contains all scraping logic.
"""

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import (
    BASE_LISTING_URL,
    PROFILE_LINK_SELECTOR,
    REVIEWER_NAME_SELECTOR,
    REVIEWER_COMPANY_SELECTOR,
    MIN_SLEEP,
    MAX_SLEEP,
    LONG_BREAK_EVERY,
    LONG_BREAK_MIN,
    LONG_BREAK_MAX,
    MAX_PROFILE_RETRIES,
    BROWSER_RESTART_AFTER,
)

from logger import logger

import random


class ClutchScraper:

    def __init__(
        self,
        browser,
        writer,
        checkpoint,
        state,
    ):

        self.browser = browser
        self.writer = writer
        self.checkpoint = checkpoint
        self.state = state

    # ======================================================
    # Sleep
    # ======================================================

    def sleep(self):

        delay = random.uniform(
            MIN_SLEEP,
            MAX_SLEEP
        )

        time.sleep(delay)

    # ======================================================
    # Long Break
    # ======================================================

    def long_break(self):

        if self.state["page"] % LONG_BREAK_EVERY != 0:
            return

        delay = random.randint(
            LONG_BREAK_MIN,
            LONG_BREAK_MAX
        )

        logger.info(
            f"Taking long break ({delay} sec)"
        )

        time.sleep(delay)

    # ======================================================
    # Open Listing Page
    # ======================================================
    
    def open_listing_page(self, page):

        if page == 1:
            url = BASE_LISTING_URL
        else:
            url = f"{BASE_LISTING_URL}?page={page}"

        logger.info("=" * 80)
        logger.info(f"Opening Page {page}")
        logger.info(url)

        return self.browser.safe_get(url)
    # ======================================================
    # Collect Profile URLs
    # ======================================================

    def collect_profile_urls(self):

        logger.info(
            "Collecting profile URLs..."
        )

        self.browser.wait.until(

            EC.presence_of_all_elements_located(

                (
                    By.CSS_SELECTOR,
                    PROFILE_LINK_SELECTOR
                )

            )

        )

        links = self.browser.driver.find_elements(

            By.CSS_SELECTOR,

            PROFILE_LINK_SELECTOR

        )

        profile_urls = []

        seen = set()

        for link in links:

            try:

                if not link.is_displayed():
                    continue

                url = link.get_attribute("href")

                if not url:
                    continue

                url = url.strip()

                if url in seen:
                    continue

                seen.add(url)

                profile_urls.append(url)

            except Exception as e:

                logger.exception(e)

        logger.info(
            f"Profiles Found : {len(profile_urls)}"
        )

        return profile_urls

    # ======================================================
    # Open Company Profile
    # ======================================================

    def open_profile(
        self,
        profile_url
    ):

        for attempt in range(
            1,
            MAX_PROFILE_RETRIES + 1
        ):

            logger.info(
                f"Attempt {attempt}/{MAX_PROFILE_RETRIES}"
            )

            success = self.browser.safe_get(
                profile_url
            )

            if not success:

                self.sleep()

                continue

            try:

                self.browser.wait.until(

                    EC.presence_of_element_located(

                        (
                            By.CSS_SELECTOR,
                            REVIEWER_NAME_SELECTOR
                        )

                    )

                )

                return True

            except TimeoutException:

                logger.warning(
                    "Reviewer section not loaded."
                )

            self.sleep()

        return False
    # ======================================================
    # Extract Reviews
    # ======================================================

    def extract_reviews(
        self,
        profile_url,
        page_number,
    ):

        reviews = []

        names = self.browser.driver.find_elements(
            By.CSS_SELECTOR,
            REVIEWER_NAME_SELECTOR
        )

        companies = self.browser.driver.find_elements(
            By.CSS_SELECTOR,
            REVIEWER_COMPANY_SELECTOR
        )

        count = min(
            len(names),
            len(companies)
        )

        logger.info(
            f"Reviews Found : {count}"
        )

        seen = set()

        for i in range(count):

            try:

                reviewer_name = names[i].text.strip()

                reviewer_company = companies[i].text.strip()

                if (
                    not reviewer_name
                    or not reviewer_company
                    or reviewer_name.strip().lower() == "anonymous"
                ):
                    continue

                key = (
                    reviewer_name,
                    reviewer_company
                )

                if key in seen:
                    continue

                seen.add(key)

                reviews.append(
                    {
                        "Page Number": page_number,
                        "Profile URL": profile_url,
                        "Reviewer Name": reviewer_name,
                        "Reviewer Company": reviewer_company,
                    }
                )

            except Exception as e:

                logger.exception(e)

        return reviews

    # ======================================================
    # Process One Profile
    # ======================================================

    def process_profile(
        self,
        profile_url,
        page_number,
    ):

        logger.info("-" * 80)
        logger.info(profile_url)

        success = self.open_profile(
            profile_url
        )

        if not success:

            logger.error(
                "Unable to open profile."
            )

            self.writer.save_failed_profile(
                page_number,
                profile_url,
                "Unable to load profile"
            )

            return

        reviews = self.extract_reviews(
            profile_url,
            page_number,
        )

        # Save immediately
        if reviews:

            self.writer.write_reviews(
                reviews
            )

            self.state["reviews_scraped"] += len(
                reviews
            )

        # Update checkpoint after every profile
        self.state["profiles_scraped"] += 1

        self.checkpoint.save(
            self.state
        )

        logger.info(
            f"Total Profiles : {self.state['profiles_scraped']}"
        )

        logger.info(
            f"Total Reviews : {self.state['reviews_scraped']}"
        )

        self.sleep()

        # Restart browser after every N profiles
        if (
            self.state["profiles_scraped"]
            % BROWSER_RESTART_AFTER
            == 0
        ):

            self.browser.restart()    

    # ======================================================
    # Scrape One Listing Page
    # ======================================================

    def scrape_page(self):

        page = self.state["page"]

        if not self.open_listing_page(page):

            logger.error(
                f"Failed to open page {page}"
            )

            self.writer.save_failed_page(
                page,
                "Unable to open listing page"
            )

            self.state["page"] += 1
            self.state["profile_index"] = 0

            self.checkpoint.save(
                self.state
            )

            return

        profile_urls = self.collect_profile_urls()

        if not profile_urls:

            logger.warning(
                "No profiles found."
            )

            self.writer.save_failed_page(
                page,
                "No profiles found"
            )

            self.state["page"] += 1
            self.state["profile_index"] = 0

            self.checkpoint.save(
                self.state
            )

            return

        total = len(profile_urls)

        start = self.state["profile_index"]

        logger.info("=" * 80)
        logger.info(
            f"Processing {total} profiles "
            f"(Starting from {start + 1})"
        )
        logger.info("=" * 80)

        for index in range(start, total):

            self.state["profile_index"] = index

            profile = profile_urls[index]

            logger.info(
                f"[{index + 1}/{total}]"
            )

            try:

                self.process_profile(
                    profile,
                    page
                )

            except Exception as e:

                logger.exception(e)

                self.writer.save_failed_profile(
                    page,
                    profile,
                    str(e)
                )

            self.checkpoint.save(
                self.state
            )

        logger.info("=" * 80)
        logger.info(
            f"Finished Page {page}"
        )
        logger.info("=" * 80)

        self.long_break()

        self.state["page"] += 1

        self.state["profile_index"] = 0

        self.checkpoint.save(
            self.state
        )

    # ======================================================
    # Run Scraper
    # ======================================================

    def run(self, end_page):

        while self.state["page"] <= end_page:

            self.scrape_page()

        logger.info("=" * 80)
        logger.info("Scraping Completed")
        logger.info("=" * 80)            