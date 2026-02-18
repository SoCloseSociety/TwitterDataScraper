<div align="center">

# TwitterDataScraper

### Scrape Twitter/X profiles at scale — no API keys needed.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/SoCloseSociety/TwitterDataScraper?style=for-the-badge&logo=github)](https://github.com/SoCloseSociety/TwitterDataScraper/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/SoCloseSociety/TwitterDataScraper?style=for-the-badge)](https://github.com/SoCloseSociety/TwitterDataScraper/issues)

A **lightweight, performant Python scraper** for extracting Twitter/X user profiles using Selenium.
Collect profile links and usernames from any Twitter/X page — followers, search results, lists, and more.

**Part of the [SoClose Open-Source Toolkit](https://github.com/SoCloseSociety)**  — automation tools built for developers, by developers.

[Getting Started](#quick-start) · [Documentation](#usage) · [Contributing](#contributing) · [Report Bug](https://github.com/SoCloseSociety/TwitterDataScraper/issues/new?template=bug_report.md) · [Request Feature](https://github.com/SoCloseSociety/TwitterDataScraper/issues/new?template=feature_request.md)

</div>

---

## Why TwitterDataScraper?

Most Twitter scraper and X scraper tools either require expensive API access, break frequently, or are bloated with unnecessary dependencies. **TwitterDataScraper** takes a different approach to web scraping:

- **Zero API cost** — Scrapes directly from the Twitter/X web interface using Selenium
- **Headless mode** — Runs invisibly in the background, perfect for servers and CI/CD
- **Smart deduplication** — O(1) set-based lookups ensure zero duplicate profiles
- **Auto-save** — Periodically saves progress to CSV so you never lose data
- **Graceful shutdown** — Press `Ctrl+C` anytime; data is saved before exit
- **Human-like behavior** — Randomized scroll pauses to mimic natural browsing patterns
- **Anti-detection** — Stealth browser fingerprint to reduce automation detection
- **Configurable** — Adjust timeouts, scroll speed, and output file via CLI flags or config
- **Clean output** — Full Twitter profile URLs and @handles exported to CSV

## Installation

### Prerequisites

- **Python 3.9+**
- **Google Chrome** browser installed

### Quick Setup

```bash
git clone https://github.com/SoCloseSociety/TwitterDataScraper.git
cd TwitterDataScraper

python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### Install as Package

```bash
pip install -e .
```

## Quick Start

### Visible mode (for manual login)

```bash
python main.py --visible -o my_profiles.csv
```

1. A Chrome window opens at the Twitter login page
2. Log in to your Twitter/X account manually
3. Navigate to the page you want to scrape (followers, search results, lists...)
4. Press **ENTER** in the terminal to start scraping
5. Press **Ctrl+C** to stop — your data is automatically saved

### Headless mode (default)

```bash
python main.py -o my_profiles.csv
```

> **Note:** Headless mode requires pre-authenticated session cookies or a publicly accessible page.

## Usage

```
usage: main.py [-h] [-o OUTPUT] [--visible] [-m MAX_ITERATIONS] [-v]

Scrape Twitter/X profile links and usernames.

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Output CSV filename (default: scraped_profiles.csv)
  --visible             Run browser in visible mode (required for manual login)
  -m, --max-iterations  Maximum scroll iterations (default: unlimited)
  -v, --verbose         Enable verbose debug logging
```

### Examples

```bash
# Scrape profiles with visible browser
python main.py --visible -o tech_influencers.csv

# Limit to 100 scroll iterations
python main.py --visible -m 100 -o results.csv

# Debug mode
python main.py --visible -v -o debug_output.csv
```

## Output Format

Clean CSV output with full URLs — ready for analysis, CRM import, or further processing:

| Column | Description | Example |
|--------|-------------|---------|
| `profile_link` | Full URL to the Twitter profile | `https://twitter.com/elonmusk` |
| `profile_username` | Twitter handle with @ prefix | `@elonmusk` |

See [examples/sample_output.csv](examples/sample_output.csv) for a complete sample.

## Project Structure

```
TwitterDataScraper/
├── twitter_scraper/        # Core package
│   ├── __init__.py         # Package exports (v1.0.0)
│   ├── browser.py          # Chrome WebDriver lifecycle management
│   ├── config.py           # Centralized configuration constants
│   ├── scraper.py          # Profile extraction engine
│   └── utils.py            # Connectivity check, logging, helpers
├── examples/               # Sample output files
├── .github/                # Issue & PR templates
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Package metadata & build config
├── LICENSE                 # MIT License
├── CONTRIBUTING.md         # Contribution guidelines
└── CODE_OF_CONDUCT.md      # Community standards
```

## Configuration

Tune the scraper to your needs in [`twitter_scraper/config.py`](twitter_scraper/config.py):

| Setting | Default | Description |
|---------|---------|-------------|
| `SCROLL_PIXELS` | 800 | Pixels to scroll per iteration |
| `SCROLL_PAUSE_MIN` | 1.5s | Minimum pause between scrolls |
| `SCROLL_PAUSE_MAX` | 3.0s | Maximum pause between scrolls |
| `MAX_STALE_ITERATIONS` | 60 | Iterations without new data before auto-stop |
| `CSV_BATCH_INTERVAL` | 10 | Save to CSV every N iterations |
| `PAGE_LOAD_TIMEOUT` | 30s | Page load timeout |

## More Open-Source Tools by SoClose

This project is part of the **SoClose Open-Source Toolkit** — a collection of Python automation and data scraping tools built for the community:

| Project | Description |
|---------|-------------|
| [PinterestBulkPostBot](https://github.com/SoCloseSociety/PinterestBulkPostBot) | Automate posting hundreds of pins to Pinterest |
| [LinkedinDataScraper](https://github.com/SoCloseSociety/LinkedinDataScraper) | Scrape LinkedIn contact info and profiles |
| [InstagramDataScraper](https://github.com/SoCloseSociety/InstagramDataScraper) | Extract Instagram profile data at scale |
| [BOT_GoogleMap_Scrapping](https://github.com/SoCloseSociety/BOT_GoogleMap_Scrapping) | Scrape business data from Google Maps |
| [FreeWorkDataScraper](https://github.com/SoCloseSociety/FreeWorkDataScraper) | Scrape job postings from FreeWork |
| [DoctolibDataScraper](https://github.com/SoCloseSociety/DoctolibDataScraper) | Extract healthcare provider data from Doctolib |
| [WhatsappSender](https://github.com/SoCloseSociety/WhatsappSender) | Automate WhatsApp message sending |

Explore all projects at **[github.com/SoCloseSociety](https://github.com/SoCloseSociety)**

## Contributing

We welcome contributions from developers worldwide! Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

- Found a bug? [Open an issue](https://github.com/SoCloseSociety/TwitterDataScraper/issues/new?template=bug_report.md)
- Have an idea? [Request a feature](https://github.com/SoCloseSociety/TwitterDataScraper/issues/new?template=feature_request.md)
- Want to contribute code? Fork, branch, and submit a PR

## Disclaimer

This tool is provided for **educational and research purposes only**. Users are responsible for ensuring their use complies with Twitter/X's [Terms of Service](https://twitter.com/en/tos) and all applicable laws and regulations. The authors are not responsible for any misuse of this software. Always scrape responsibly and respect rate limits.

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### Built by SoClose

**Digital solutions & automation studio — building open-source tools for the community.**

[![Website](https://img.shields.io/badge/Website-soclose.co-575ECF?style=for-the-badge&logo=googlechrome&logoColor=white)](https://soclose.co)
[![GitHub](https://img.shields.io/badge/GitHub-SoCloseSociety-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SoCloseSociety)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-SoClose-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/company/soclose-agency)
[![Twitter](https://img.shields.io/badge/Twitter-@SoCloseAgency-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/SoCloseAgency)
[![Email](https://img.shields.io/badge/Email-contact@soclose.co-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:contact@soclose.co)

If this project helped you, consider giving it a **star** — it helps others discover our tools.

</div>
