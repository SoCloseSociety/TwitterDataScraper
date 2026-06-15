# CLAUDE.md -- TwitterDataScraper

## 1. Project Identity

**Name:** TwitterDataScraper -- Twitter/X Profile Scraper
**Role:** Selenium-based tool to scrape Twitter/X profile URLs from feeds, followers, and search results with O(1) dedup and auto-save.
**Author:** SoClose Society (https://soclose.co)
**License:** MIT

### Stack

- **Language:** Python 3.9+
- **Browser:** Selenium 4.15+ with webdriver-manager
- **Parsing:** BeautifulSoup4
- **Data:** pandas
- **Architecture:** Modular (5 files, ~475 LOC)

### Project Structure

```
main.py (88 LOC)              CLI entry point
twitter_scraper/
├── __init__.py               Package exports
├── browser.py (75 LOC)       BrowserManager context manager
├── scraper.py (217 LOC)      TwitterProfileScraper core
├── config.py (31 LOC)        Constants (delays, timeouts, patterns)
└── utils.py (48 LOC)         Connectivity checks, logging, helpers
```

### Critical Files

- `twitter_scraper/scraper.py` -- Core scrolling + extraction logic
- `twitter_scraper/config.py` -- Timing constants tuned for anti-detection

## 2-5. Standard Workflow

- Enter plan mode for non-trivial tasks
- Test in visible mode first (`--visible`) to verify login works
- Never reduce scroll delays below 1.5s -- triggers anti-bot detection
- Track tasks in `tasks/todo.md`, lessons in `tasks/lessons.md`

## 6. Project-Specific Rules

### Dev Commands
```bash
pip install -r requirements.txt
python main.py                    # Headless mode
python main.py --visible          # Visible (for manual login)
python main.py -o profiles.csv   # Custom output
python main.py -m 100 -v         # Max 100 iterations, verbose
```

### Config Constants (config.py)
- SCROLL_PAUSE_MIN=1.5, SCROLL_PAUSE_MAX=3.0
- MAX_STALE_ITERATIONS=60
- CSV_BATCH_INTERVAL=10
- PROFILE_HREF_PATTERN -- Regex for Twitter profile paths

### Known Fragile Areas
- Twitter DOM changes can break profile extraction silently
- Manual login required in visible mode (no automated auth)
- Stale detection: auto-stops after 60 iterations with no new profiles

## Neo Connector (auto)
Ce projet expose `NEO_CONNECTOR.md` : le manifeste machine-lisible de TOUS ses
endpoints/auth/env, consommé par NeoBot pour se câbler automatiquement.
- NOTE : ce repo n'expose AUCUNE API HTTP/webhook/SSE/WS -- c'est un scraper CLI Selenium pur.
  Il ne doit PAS être câblé comme outils HTTP Neo (voir verdict dans NEO_CONNECTOR.md).
- RÈGLE : à chaque ajout/suppression/modif d'un endpoint, d'une auth ou d'une env var,
  régénère le manifeste via `/neo-connector` (ou le prompt dans .claude/skills/neo-connector).
- Ne jamais éditer NEO_CONNECTOR.md à la main : il est généré.
- Le hook pre-commit (.git/hooks/pre-commit) avertit si des routes ont changé sans MAJ du manifeste.

## 7. Core Principles

- Simplicity First, No Laziness, Minimal Impact
- Never use em dashes (use -- instead)
- Never reduce anti-detection delays
