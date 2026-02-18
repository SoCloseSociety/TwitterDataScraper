#!/usr/bin/env python3
"""TwitterDataScraper - Scrape Twitter/X profile data with Selenium.

Part of the SoClose Open-Source Toolkit.
https://github.com/SoCloseSociety/TwitterDataScraper | https://soclose.co
"""

from __future__ import annotations

import argparse
import logging
import sys

from twitter_scraper import BrowserManager, TwitterProfileScraper
from twitter_scraper.utils import is_connected, sanitize_filename, setup_logging

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape Twitter/X profile links and usernames.",
        epilog="Part of the SoClose Open-Source Toolkit | https://soclose.co",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="scraped_profiles.csv",
        help="Output CSV filename (default: scraped_profiles.csv)",
    )
    parser.add_argument(
        "--visible",
        action="store_true",
        help="Run browser in visible mode (required for manual login)",
    )
    parser.add_argument(
        "-m",
        "--max-iterations",
        type=int,
        default=None,
        help="Maximum number of scroll iterations (default: unlimited)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose debug logging",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(verbose=args.verbose)

    if not is_connected():
        print("No internet connection detected. Please check your network.")
        sys.exit(1)

    output = args.output
    if not output.endswith(".csv"):
        output += ".csv"
    output = sanitize_filename(output.removesuffix(".csv")) + ".csv"

    headless = not args.visible

    if headless:
        logger.warning(
            "Running in headless mode. Twitter requires authentication for most pages. "
            "Use --visible flag if you need to log in manually."
        )

    with BrowserManager(headless=headless) as driver:
        scraper = TwitterProfileScraper(driver=driver, output_file=output)
        scraper.navigate_to_login()

        if not headless:
            scraper.wait_for_user_ready()

        scraper.scrape(max_iterations=args.max_iterations)

    print(f"\nDone! Results saved to: {output}")


if __name__ == "__main__":
    main()
