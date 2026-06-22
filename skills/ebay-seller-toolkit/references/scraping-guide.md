# Ecommerce Data Scraping Guide

## Overview

This guide covers techniques for collecting product data from ecommerce websites using compliant methods. All data collection activities must comply with the target website's `robots.txt` and terms of service. Always prefer official APIs when available.

## Ethical Scraping Principles

1. **Respect robots.txt** — Check and obey the site's crawling rules before any request (see enforcement code below)
2. **Rate limiting** — Maximum 1 request per 2 seconds per domain
3. **Prefer APIs** — Use official APIs (Amazon Product Advertising API, eBay Browse API, etc.) when available
4. **Minimal footprint** — Only collect data that is needed
5. **Respect authentication boundaries** — Do not access content behind login walls or paywalls
6. **Respect security mechanisms** — Do not attempt to work around WAF protections, CAPTCHAs, or any anti-bot systems. If access is blocked, stop and use the platform's official API instead.
7. **Data retention** — Retain scraped data for a maximum of **30 days**. Implement automated cleanup to delete data older than 30 days. Each data file should include a `scraped_at` timestamp to facilitate cleanup.

### robots.txt Compliance Check (Mandatory)

Before scraping any URL, verify it is allowed by the target site's `robots.txt`. If disallowed, skip the URL and log the reason.

```python
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def is_url_allowed(url, user_agent="*"):
    """Check if a URL is allowed by the site's robots.txt. Returns True only if explicitly allowed."""
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        # If robots.txt cannot be fetched, assume disallowed for safety
        return False
```

**Usage**: Call `is_url_allowed(url)` before every scraping request. Abort and log if it returns `False`.

## Terms of Service (ToS) Risk Disclaimer

> **Important**: Web scraping may violate the Terms of Service of certain ecommerce platforms. Before scraping any platform, review its ToS regarding automated data collection. Some platforms (e.g., Amazon, eBay) explicitly prohibit scraping in their ToS and may ban accounts or take legal action against violators.
>
> **Recommended approach**:
> - **Always prefer official APIs** (eBay Browse API, Amazon Product Advertising API, etc.) over scraping.
> - If no official API is available, ensure scraping is limited to publicly accessible data and complies with robots.txt.
> - Do not scrape data behind login walls or paywalls.
> - The user assumes all responsibility for compliance with applicable laws and platform terms of service.
> - This guide is provided for educational purposes. The authors are not liable for any misuse.

## Technology Stack

### Recommended Tools

| Tool | Use Case |
|------|----------|
| Official Platform APIs | Preferred method — structured, authorized data access |
| Playwright (Python) | JS-rendered pages, dynamic content (with robots.txt check) |
| Requests + BeautifulSoup | Simple static pages (with robots.txt check) |
| Scrapy | Large-scale structured scraping (with built-in robots.txt support) |

### Browser Automation with Playwright

```python
from playwright.sync_api import sync_playwright

def scrape_product(url):
    # Always check robots.txt before scraping
    if not is_url_allowed(url):
        print(f"Skipped (disallowed by robots.txt): {url}")
        return None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()  # Use browser default User-Agent
        page = context.new_page()
        page.goto(url, wait_until="networkidle")

        # Extract data
        title = page.query_selector("h1").inner_text()
        price = page.query_selector(".price").inner_text()

        browser.close()
        return {"title": title, "price": price}
```

## Platform-Specific Selectors

### Amazon

```python
AMAZON_SELECTORS = {
    "title": "#productTitle",
    "price": ".a-price .a-offscreen",
    "rating": "#acrPopover .a-size-base",
    "review_count": "#acrCustomerReviewText",
    "availability": "#availability span",
    "image": "#landingImage"
}
```

### eBay

```python
EBAY_SELECTORS = {
    "title": "h1.x-item-title__mainTitle",
    "price": ".x-price-primary span",
    "condition": ".x-item-condition-text span",
    "seller": ".x-sellercard-atf__info__about-seller a",
    "shipping": ".ux-labels-values--shipping .ux-textspans--BOLD",
    "image": ".ux-image-carousel-item img"
}
```

### JD (京东)

```python
JD_SELECTORS = {
    "title": ".sku-name",
    "price": ".price .p-price span",
    "shop": ".J-hove-wrap .item .name a",
    "rating": ".comment-percent .count",
    "image": "#spec-img"
}
```

### General Ecommerce

```python
GENERAL_SELECTORS = {
    "title": ["h1", ".product-title", ".product-name", "[data-testid='product-title']"],
    "price": [".price", ".product-price", "[data-testid='price']", ".sale-price"],
    "image": [".product-image img", ".gallery img", "[data-testid='product-image']"]
}
```

## Compliant Request Practices

### Rate Limiting

```python
import time

def rate_limited_request(page, url, min_delay=2):
    """Wait at least min_delay seconds between requests to respect rate limits."""
    time.sleep(min_delay)
    page.goto(url, wait_until="networkidle")
```

## Output Format

Scraped data should be structured as JSON:

```json
{
    "product": {
        "title": "Product Name",
        "price": 29.99,
        "currency": "USD",
        "url": "https://...",
        "image_url": "https://...",
        "seller": "Store Name",
        "rating": 4.5,
        "review_count": 1234,
        "availability": "In Stock",
        "scraped_at": "2026-03-28T14:00:00Z"
    }
}
```

## Data Retention & Cleanup

Scraped data must be managed with a clear retention policy:

- **Maximum retention period**: 30 days from `scraped_at` timestamp
- **Automated cleanup**: Implement a cleanup routine that runs periodically to delete expired data
- **Cleanup example**:

```python
import os
import json
from datetime import datetime, timedelta, timezone

def cleanup_expired_data(data_dir, max_age_days=30):
    """Delete JSON data files older than max_age_days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    deleted = 0
    for filename in os.listdir(data_dir):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(data_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            scraped_at = data.get("scraped_at") or data.get("product", {}).get("scraped_at")
            if scraped_at:
                ts = datetime.fromisoformat(scraped_at.replace("Z", "+00:00"))
                if ts < cutoff:
                    os.remove(filepath)
                    deleted += 1
        except Exception:
            continue
    print(f"Cleanup complete: {deleted} expired file(s) removed.")
```

## Batch Scraping

For scraping multiple products, use the `scripts/price_scraper.py` script which handles:
- robots.txt compliance check before each request
- Rate limiting per domain (minimum 2-second delay)
- Automatic retry on failure
- Structured JSON output with timestamps
- Progress reporting
