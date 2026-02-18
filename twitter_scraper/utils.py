"""Utility functions for TwitterDataScraper."""

from __future__ import annotations

import logging
import re
import socket

from twitter_scraper.config import (
    CONNECTIVITY_CHECK_HOST,
    CONNECTIVITY_CHECK_PORT,
    CONNECTIVITY_TIMEOUT,
)


def is_connected() -> bool:
    """Check internet connectivity by attempting a TCP connection to 1.1.1.1."""
    try:
        conn = socket.create_connection(
            (CONNECTIVITY_CHECK_HOST, CONNECTIVITY_CHECK_PORT),
            timeout=CONNECTIVITY_TIMEOUT,
        )
        conn.close()
        return True
    except (socket.timeout, OSError):
        return False


def sanitize_filename(name: str) -> str:
    """Remove invalid characters from a filename.

    Replaces characters not allowed in filenames with underscores,
    strips leading/trailing dots and spaces, and defaults to 'output'
    if the result is empty.
    """
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", name)
    sanitized = sanitized.strip(". ")
    return sanitized or "output"


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the scraper."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
