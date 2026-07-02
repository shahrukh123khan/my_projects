"""
config.py

Central configuration file for the Clutch scraper.
Modify values here instead of changing the scraper code.
"""

# ==========================================================
# WEBSITE
# ==========================================================

BASE_LISTING_URL = "https://clutch.co/agencies/digital-marketing"

# ==========================================================
# SCRAPING
# ==========================================================

START_PAGE = 1
END_PAGE = 2522

HEADLESS = False              # Set True when running on server
CHROME_VERSION = 149

# ==========================================================
# WAITS (seconds)
# ==========================================================

PAGE_LOAD_TIMEOUT = 60
ELEMENT_TIMEOUT = 20

# Random sleep between profile requests
MIN_SLEEP = 1.5
MAX_SLEEP = 3.5

# Long break after every N pages
LONG_BREAK_EVERY = 25
LONG_BREAK_MIN = 20
LONG_BREAK_MAX = 40

# ==========================================================
# RETRIES
# ==========================================================

MAX_PAGE_RETRIES = 3
MAX_PROFILE_RETRIES = 3

# Restart browser after every N profiles
BROWSER_RESTART_AFTER = 500

# ==========================================================
# FILES
# ==========================================================

OUTPUT_CSV = "output/clutch_reviews.csv"

CHECKPOINT_FILE = "output/checkpoint.json"

FAILED_PAGES_CSV = "output/failed_pages.csv"

FAILED_PROFILES_CSV = "output/failed_profiles.csv"

LOG_FILE = "logs/scraper.log"

SCREENSHOT_DIR = "screenshots"

# ==========================================================
# CSV
# ==========================================================

CSV_ENCODING = "utf-8-sig"

CSV_HEADERS = [
    "Page Number",
    "Profile URL",
    "Reviewer Name",
    "Reviewer Company",
]

# ==========================================================
# SELECTORS
# ==========================================================

PROFILE_LINK_SELECTOR = (
    "a.provider__title-link.directory_profile"
)

REVIEWER_NAME_SELECTOR = (
    "div.reviewer_card--name"
)

REVIEWER_COMPANY_SELECTOR = (
    "div.reviewer_position"
)

# ==========================================================
# DIRECTORIES
# ==========================================================

OUTPUT_DIR = "output"
LOG_DIR = "logs"

# ==========================================================
# CREATE DIRECTORIES
# ==========================================================

from pathlib import Path

Path(OUTPUT_DIR).mkdir(
    parents=True,
    exist_ok=True,
)

Path(LOG_DIR).mkdir(
    parents=True,
    exist_ok=True,
)

Path(SCREENSHOT_DIR).mkdir(
    parents=True,
    exist_ok=True,
)