"""
checkpoint.py

Handles saving and loading scraper progress.
"""

import json
from pathlib import Path

from config import CHECKPOINT_FILE
from logger import logger


class Checkpoint:

    def __init__(self):

        self.file = Path(CHECKPOINT_FILE)

    # ======================================================
    # Default State
    # ======================================================

    def default_state(self):

        return {
            "page": 1,
            "profile_index": 0,
            "profiles_scraped": 0,
            "reviews_scraped": 0,
        }

    # ======================================================
    # Load Checkpoint
    # ======================================================

    def load(self):

        if not self.file.exists():

            logger.info(
                "No checkpoint found. Starting from page 1."
            )

            return self.default_state()

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                state = json.load(f)

            logger.info(
                f"Resuming from page {state['page']} "
                f"profile {state['profile_index'] + 1}"
            )

            return state

        except Exception as e:

            logger.exception(e)

            logger.warning(
                "Checkpoint is corrupted. Starting from beginning."
            )

            return self.default_state()

    # ======================================================
    # Save Checkpoint
    # ======================================================

    def save(self, state):

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    state,
                    f,
                    indent=4
                )

        except Exception as e:

            logger.exception(e)

    # ======================================================
    # Reset Checkpoint
    # ======================================================

    def reset(self):

        try:

            if self.file.exists():

                self.file.unlink()

                logger.info(
                    "Checkpoint removed."
                )

        except Exception as e:

            logger.exception(e)