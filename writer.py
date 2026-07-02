"""
writer.py

Handles writing scraped data to CSV files.
"""

import csv
from pathlib import Path

from config import (
    OUTPUT_CSV,
    FAILED_PAGES_CSV,
    FAILED_PROFILES_CSV,
    CSV_HEADERS,
    CSV_ENCODING,
)

from logger import logger


class Writer:

    def __init__(self):

        self.create_files()

        # -----------------------------
        # Main CSV
        # -----------------------------
        self.output_file = open(
            OUTPUT_CSV,
            "a",
            newline="",
            encoding=CSV_ENCODING
        )

        self.output_writer = csv.DictWriter(
            self.output_file,
            fieldnames=CSV_HEADERS
        )

        # -----------------------------
        # Failed Profiles
        # -----------------------------
        self.failed_profile_file = open(
            FAILED_PROFILES_CSV,
            "a",
            newline="",
            encoding=CSV_ENCODING
        )

        self.failed_profile_writer = csv.writer(
            self.failed_profile_file
        )

        # -----------------------------
        # Failed Pages
        # -----------------------------
        self.failed_page_file = open(
            FAILED_PAGES_CSV,
            "a",
            newline="",
            encoding=CSV_ENCODING
        )

        self.failed_page_writer = csv.writer(
            self.failed_page_file
        )

    # =====================================================
    # Create CSV files if they don't exist
    # =====================================================

    def create_files(self):

        files = [

            (
                OUTPUT_CSV,
                CSV_HEADERS
            ),

            (
                FAILED_PROFILES_CSV,
                [
                    "Page Number",
                    "Profile URL",
                    "Reason"
                ]
            ),

            (
                FAILED_PAGES_CSV,
                [
                    "Page Number",
                    "Reason"
                ]
            )

        ]

        for file_name, header in files:

            path = Path(file_name)

            if path.exists():

                continue

            with open(
                path,
                "w",
                newline="",
                encoding=CSV_ENCODING
            ) as f:

                writer = csv.writer(f)

                writer.writerow(header)

    # =====================================================
    # Save Reviews
    # =====================================================

    def write_reviews(
        self,
        reviews
    ):

        if not reviews:

            return

        self.output_writer.writerows(
            reviews
        )

        self.output_file.flush()

        logger.info(
            f"Saved {len(reviews)} reviews."
        )

    # =====================================================
    # Failed Profile
    # =====================================================

    def save_failed_profile(
        self,
        page,
        profile,
        reason
    ):

        self.failed_profile_writer.writerow(

            [
                page,
                profile,
                reason
            ]

        )

        self.failed_profile_file.flush()

    # =====================================================
    # Failed Page
    # =====================================================

    def save_failed_page(
        self,
        page,
        reason
    ):

        self.failed_page_writer.writerow(

            [
                page,
                reason
            ]

        )

        self.failed_page_file.flush()

    # =====================================================
    # Close Files
    # =====================================================

    def close(self):

        self.output_file.close()

        self.failed_profile_file.close()

        self.failed_page_file.close()