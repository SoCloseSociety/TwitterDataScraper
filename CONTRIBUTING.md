# Contributing to TwitterDataScraper

Thank you for your interest in contributing to **TwitterDataScraper**! This project is part of the [SoClose Open-Source Toolkit](https://github.com/SoCloseSociety) and we welcome contributions from the community.

## Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold these standards.

## Getting Started

### Prerequisites

- Python 3.9+
- Google Chrome
- Git

### Local Development Setup

```bash
# 1. Fork & clone
git clone https://github.com/YOUR_USERNAME/TwitterDataScraper.git
cd TwitterDataScraper

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install with dev dependencies
pip install -e ".[dev]"
```

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check [existing issues](https://github.com/SoCloseSociety/TwitterDataScraper/issues) to avoid duplicates.

When reporting a bug, include:
- Python version (`python --version`)
- Operating system
- Chrome version
- Steps to reproduce
- Expected vs actual behavior
- Error logs (use `--verbose` flag)

### Suggesting Features

Open an issue with the **Feature Request** template and describe:
- The use case
- Expected behavior
- Why this would benefit other users

### Submitting Code

1. **Fork** the repository
2. **Create a branch** from `main`:
   - `fix/description` for bug fixes
   - `feature/description` for new features
   - `docs/description` for documentation
3. **Make your changes** with clear, descriptive commits
4. **Test** your changes locally
5. **Submit a Pull Request** using the PR template

### Commit Messages

- Use present tense: "Add feature" not "Added feature"
- Keep the first line under 72 characters
- Reference issues: "Fix #123: description"

### Code Standards

- Follow PEP 8 conventions
- Use type hints for function signatures
- Add docstrings to public functions and classes
- Keep functions focused and small

## Need Help?

- Open a [GitHub Discussion](https://github.com/SoCloseSociety/TwitterDataScraper/discussions)
- Email: contact@soclose.co
- Explore our other tools: [github.com/SoCloseSociety](https://github.com/SoCloseSociety)

---

*Happy contributing!* — The [SoClose](https://soclose.co) team
