#!/bin/bash
# ============================================================================
# GitHub Repository SEO & Branding Setup for TwitterDataScraper
# Run this script after pushing to GitHub to optimize discoverability.
# Requires: gh CLI (https://cli.github.com) authenticated with your account.
# ============================================================================

REPO="SoCloseSociety/TwitterDataScraper"

echo "=== Setting up GitHub repo: $REPO ==="

# 1. Update repo description and metadata
echo "[1/4] Updating repository description..."
gh repo edit "$REPO" \
  --description "Lightweight Python scraper for Twitter/X user profiles using Selenium. Extract profile links and usernames at scale — no API keys required. Built by SoClose." \
  --homepage "https://soclose.co"

# 2. Set repository topics (SEO keywords for GitHub search)
echo "[2/4] Setting repository topics..."
gh api -X PUT "repos/$REPO/topics" \
  -f '{"names":["twitter-scraper","x-scraper","twitter","python","selenium","web-scraping","data-extraction","scraper","automation","social-media-scraper","twitter-data","profile-scraper","python-scraper","open-source","soclose"]}' \
  --silent

# 3. Enable useful repo features
echo "[3/4] Configuring repository features..."
gh repo edit "$REPO" \
  --enable-issues \
  --enable-wiki=false \
  --enable-discussions

# 4. Verify setup
echo "[4/4] Verifying setup..."
echo ""
echo "Repository: https://github.com/$REPO"
echo ""
gh repo view "$REPO" --json description,homepageUrl,repositoryTopics \
  --template '
Description: {{.description}}
Homepage:    {{.homepageUrl}}
Topics:      {{range .repositoryTopics}}{{.name}} {{end}}
'

echo ""
echo "=== Done! ==="
echo ""
echo "MANUAL STEPS REMAINING:"
echo "  1. Go to https://github.com/$REPO/settings"
echo "  2. Upload a Social Preview image (1280x640px recommended)"
echo "     - Use dark background (#1b1b1b)"
echo "     - Title: 'TwitterDataScraper'"
echo "     - Subtitle: 'Scrape Twitter/X profiles with Python'"
echo "     - Add SoClose logo and accent color (#575ECF)"
echo "  3. Pin this repo on the SoCloseSociety org profile"
