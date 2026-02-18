"""Core scraping logic for Twitter/X profile extraction."""

from __future__ import annotations

import logging
import random
import re
import signal
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from twitter_scraper.config import (
    CSV_BATCH_INTERVAL,
    MAX_STALE_ITERATIONS,
    PROFILE_HREF_PATTERN,
    PROFILE_LINK_SELECTOR,
    SCROLL_PAUSE_MAX,
    SCROLL_PAUSE_MIN,
    SCROLL_PIXELS,
    TWITTER_BASE_URL,
    TWITTER_LOGIN_URL,
)

logger = logging.getLogger(__name__)

_profile_href_re = re.compile(PROFILE_HREF_PATTERN)


@dataclass(frozen=True)
class ScrapedProfile:
    """A scraped Twitter/X profile."""
    link: str
    username: str


class TwitterProfileScraper:
    """Scrapes Twitter/X profile links and usernames from the current page.

    The scraper scrolls the page, extracts profile links, deduplicates them,
    and periodically saves results to a CSV file. It handles graceful shutdown
    on Ctrl+C by saving collected data before exiting.

    Attributes:
        driver: Selenium WebDriver instance.
        output_file: Path to the output CSV file.
    """

    def __init__(self, driver: WebDriver, output_file: str) -> None:
        self.driver = driver
        self.output_file = Path(output_file)
        self._seen_usernames: set = set()
        self._results: list = []
        self._stop_requested = False
        self._previous_handler = None

    def navigate_to_login(self) -> None:
        """Open the Twitter login page."""
        logger.info("Navigating to Twitter login page...")
        self.driver.get(TWITTER_LOGIN_URL)

    def wait_for_user_ready(self) -> None:
        """Wait for user confirmation to start scraping."""
        print("\nLog in to Twitter, then navigate to the page you want to scrape.")
        input("Press ENTER when ready to start scraping...")

    def scrape(self, max_iterations: Optional[int] = None) -> None:
        """Main scraping loop. Scrolls the page and extracts profiles.

        Periodically saves results to CSV. Handles Ctrl+C gracefully
        by saving data before exit. Automatically stops when no new
        profiles are found for MAX_STALE_ITERATIONS consecutive scrolls.

        Args:
            max_iterations: Maximum number of scroll iterations.
                None for unlimited, 0 to stop immediately.
        """
        self._install_signal_handler()

        try:
            self._run_scrape_loop(max_iterations)
        finally:
            self._save_to_csv()
            self._restore_signal_handler()
            logger.info(
                "Scraping complete. Total profiles: %d", len(self._seen_usernames)
            )

    def _run_scrape_loop(self, max_iterations: Optional[int]) -> None:
        """Internal loop that performs the actual scraping."""
        iteration = 0
        stale_count = 0

        logger.info("Starting scrape loop...")

        while not self._stop_requested:
            if max_iterations is not None and iteration >= max_iterations:
                logger.info("Reached max iterations (%d). Stopping.", max_iterations)
                break

            iteration += 1
            new_found = self._extract_profiles()

            if new_found > 0:
                stale_count = 0
                logger.info(
                    "Iteration %d: +%d new profiles (total: %d)",
                    iteration,
                    new_found,
                    len(self._seen_usernames),
                )
            else:
                stale_count += 1

            if stale_count >= MAX_STALE_ITERATIONS:
                logger.info(
                    "No new profiles found for %d consecutive iterations. Stopping.",
                    MAX_STALE_ITERATIONS,
                )
                break

            if iteration % CSV_BATCH_INTERVAL == 0:
                self._save_to_csv()

            self._scroll_down()
            self._random_pause()

    def _extract_profiles(self) -> int:
        """Extract profile links from the current page source.

        Returns:
            Number of new profiles found in this iteration.
        """
        new_count = 0
        try:
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            links = soup.select(PROFILE_LINK_SELECTOR)

            for tag in links:
                href = tag.get("href")
                text = tag.get_text(strip=True)

                if not href or not text:
                    continue

                if (
                    text.startswith("@")
                    and _profile_href_re.match(href)
                    and text not in self._seen_usernames
                ):
                    full_link = TWITTER_BASE_URL + href
                    self._seen_usernames.add(text)
                    self._results.append(
                        ScrapedProfile(link=full_link, username=text)
                    )
                    new_count += 1

        except WebDriverException as e:
            logger.warning("Browser error during extraction: %s", e)
        except Exception as e:
            logger.error("Unexpected error during extraction: %s", e)

        return new_count

    def _scroll_down(self) -> None:
        """Scroll down the page using JavaScript."""
        try:
            self.driver.execute_script(f"window.scrollBy(0, {SCROLL_PIXELS});")
        except WebDriverException as e:
            logger.warning("Scroll failed: %s", e)

    def _random_pause(self) -> None:
        """Wait a random duration between scrolls to mimic human behavior."""
        pause = random.uniform(SCROLL_PAUSE_MIN, SCROLL_PAUSE_MAX)
        time.sleep(pause)

    def _save_to_csv(self) -> None:
        """Save all collected profiles to CSV file (overwrites previous save)."""
        if not self._results:
            return

        try:
            df = pd.DataFrame(
                [
                    {"profile_link": p.link, "profile_username": p.username}
                    for p in self._results
                ]
            )
            df.to_csv(self.output_file, index=False, encoding="utf-8")
            logger.info(
                "Saved %d profiles to %s", len(self._results), self.output_file
            )
        except OSError as e:
            logger.error("Failed to save CSV: %s", e)

    def _install_signal_handler(self) -> None:
        """Install a SIGINT handler for graceful shutdown. Saves the previous handler."""
        self._previous_handler = signal.getsignal(signal.SIGINT)

        def handler(signum, frame):
            logger.info("Stop requested (Ctrl+C). Finishing up...")
            self._stop_requested = True

        signal.signal(signal.SIGINT, handler)

    def _restore_signal_handler(self) -> None:
        """Restore the previous SIGINT handler."""
        if self._previous_handler is not None:
            signal.signal(signal.SIGINT, self._previous_handler)
            self._previous_handler = None
