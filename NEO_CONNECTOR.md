# NEO_CONNECTOR -- TwitterDataScraper
- service: twitterscraper
- base_url_prod: N/A (no network service -- local CLI tool)
- auth: none (no service auth; Twitter/X login is done manually in the browser via `--visible`)
- env_required: []
- generated_at:

## Endpoints

NONE. This repo exposes **no HTTP API, no webhook, no SSE/WebSocket, no cron, no queue,
and no network server of any kind**. It is a pure command-line Selenium scraper.

Proof from code:
- `main.py` is an `argparse` CLI entry point (`def main()` under `if __name__ == "__main__":`),
  no server, no `app`, no `listen()`.
- `requirements.txt` / `pyproject.toml` dependencies are only `selenium`, `webdriver-manager`,
  `beautifulsoup4`, `pandas` -- no Flask/FastAPI/aiohttp/uvicorn/Express.
- Repo-wide grep for `flask|fastapi|aiohttp|uvicorn|@app\.|@router|app\.route|http.server|socketserver|webhook|websocket|listen(` -> no matches.
- Only outbound network use: `twitter_scraper/utils.py:is_connected()` opens a TCP socket to
  `1.1.1.1:53` purely as a connectivity check, and Selenium drives a Chrome browser against
  `twitter.com`. Neither is an endpoint Neo can call.

### Invocation surface (CLI only -- NOT a Neo HTTP tool)

Run via `python main.py` (see `main.py:parse_args`):
| flag | type | required | default | description |
|------|------|----------|---------|-------------|
| `-o`, `--output` | str | no | `scraped_profiles.csv` | Output CSV filename |
| `--visible` | bool flag | no | false (headless) | Visible browser (required for manual login) |
| `-m`, `--max-iterations` | int | no | unlimited | Max scroll iterations |
| `-v`, `--verbose` | bool flag | no | false | Verbose debug logging |

Output: a CSV file on local disk (`scraped_profiles.csv` by default) containing scraped
Twitter/X profile links/usernames. No JSON response, no job id, no polling.

## Flows

None. There is no `generate -> poll status -> fetch result` flow. The tool runs synchronously
in-process: launch browser -> (manual login if `--visible`) -> scroll + extract -> batch-write
CSV (`CSV_BATCH_INTERVAL=10`) -> auto-stop after `MAX_STALE_ITERATIONS=60` with no new profiles.

## Gaps

None material. There are no env vars, no API keys, and no production base URL because the
project is not a service. `TWITTER_BASE_URL = "https://twitter.com"` in
`twitter_scraper/config.py` is the scrape target, not a service Neo would call.

## Recap

- Endpoints found: **0**.
- Already covered vs new: N/A -- nothing to wire.
- WIRING VERDICT: **Do NOT wire this repo as Neo HTTP tools.** It is a standalone CLI Selenium
  scraper with no callable network interface. If automation is ever desired, it could only be
  invoked as a subprocess/CLI job (with a manual-login caveat in headless mode), not as an
  HTTP/webhook integration in `bot/integrations.py`.
