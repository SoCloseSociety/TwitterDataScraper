from user_agents import get_random_user_agent

TWITTER_LOGIN_URL = "https://twitter.com/i/flow/login"
TWITTER_BASE_URL = "https://twitter.com"

# Browser settings
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 5

# Scrolling
SCROLL_PIXELS = 800
SCROLL_PAUSE_MIN = 1.5
SCROLL_PAUSE_MAX = 3.0

# Scraping
MAX_STALE_ITERATIONS = 60
CSV_BATCH_INTERVAL = 10
CONNECTIVITY_CHECK_HOST = "1.1.1.1"
CONNECTIVITY_CHECK_PORT = 80
CONNECTIVITY_TIMEOUT = 3

# CSS / HTML selectors
PROFILE_LINK_SELECTOR = 'a[role="link"]'
PROFILE_HREF_PATTERN = r"^/[A-Za-z0-9_]{1,15}$"

# User agent (Chrome 131 - January 2025)
USER_AGENT = get_random_user_agent()
