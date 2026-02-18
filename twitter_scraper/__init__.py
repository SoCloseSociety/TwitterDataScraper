"""TwitterDataScraper - A lightweight Python scraper for Twitter/X profiles.

Part of the SoClose Open-Source Toolkit.
https://github.com/SoCloseSociety | https://soclose.co
"""

from __future__ import annotations

__version__ = "1.0.0"
__author__ = "SoCloseSociety"
__url__ = "https://github.com/SoCloseSociety/TwitterDataScraper"

from twitter_scraper.browser import BrowserManager
from twitter_scraper.scraper import TwitterProfileScraper

__all__ = ["BrowserManager", "TwitterProfileScraper"]
