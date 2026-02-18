"""Browser lifecycle management for TwitterDataScraper."""

from __future__ import annotations

import logging
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from twitter_scraper.config import (
    IMPLICIT_WAIT,
    PAGE_LOAD_TIMEOUT,
    USER_AGENT,
)

logger = logging.getLogger(__name__)


class BrowserManager:
    """Context manager for Chrome WebDriver lifecycle.

    Usage:
        with BrowserManager(headless=True) as driver:
            driver.get("https://twitter.com")
    """

    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None

    def _create_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"--user-agent={USER_AGENT}")
        options.add_experimental_option(
            "excludeSwitches", ["enable-logging", "enable-automation"]
        )
        options.add_experimental_option("useAutomationExtension", False)

        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")

        return options

    def _create_driver(self) -> webdriver.Chrome:
        options = self._create_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        return driver

    def __enter__(self) -> webdriver.Chrome:
        logger.info("Starting Chrome browser (headless=%s)...", self.headless)
        self.driver = self._create_driver()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.driver:
            logger.info("Closing browser...")
            try:
                self.driver.quit()
            except (OSError, WebDriverException):
                logger.warning("Browser already closed or failed to quit.")
        return False
