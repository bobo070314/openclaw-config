#!/usr/bin/env python3
"""
Cross-Platform Price Scraper

Scrapes and compares product prices across multiple ecommerce platforms.
Requires: playwright (pip install playwright && playwright install chromium)

Usage:
    python price_scraper.py --query "iPhone 15 Pro Max 256GB" --platforms amazon,ebay
    python price_scraper.py --query "Nintendo Switch OLED" --max-results 5 --output results.json
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: playwright is required. Install with:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)


PLATFORM_CONFIGS = {
    "amazon": {
        "search_url": "https://www.amazon.com/s?k={query}",
        "selectors": {
            "items": "[data-component-type='s-search-result']",
            "title": "h2 a span",
            "price": ".a-price .a-offscreen",
            "link": "h2 a",
            "image": ".s-image",
            "rating": ".a-icon-alt",
        },
        "base_url": "https://www.amazon.com",
    },
    "ebay": {
        "search_url": "https://www.ebay.com/sch/i.html?_nkw={query}&_sop=15",
        "selectors": {
            "items": ".s-item",
            "title": ".s-item__title span",
            "price": ".s-item__price",
            "link": ".s-item__link",
            "image": ".s-item__image-img",
            "shipping": ".s-item__shipping",
        },
        "base_url": "https://www.ebay.com",
    },
}


def is_url_allowed(url, user_agent="*"):
    """Check if a URL is allowed by the site's robots.txt."""
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        return False


def rate_limited_wait(min_delay=2):
    """Wait a fixed delay to respect rate limits."""
    time.sleep(min_delay)


def scrape_platform(page, platform, query, max_results=5):
    """Scrape product listings from a single platform."""
    config = PLATFORM_CONFIGS.get(platform)
    if not config:
        print(f"Warning: Platform '{platform}' not configured, skipping.")
        return []

    search_url = config["search_url"].format(query=query.replace(" ", "+"))
    selectors = config["selectors"]

    # Check robots.txt compliance
    if not is_url_allowed(search_url):
        print(f"Skipped {platform}: URL disallowed by robots.txt")
        return []

    try:
        rate_limited_wait()
        page.goto(search_url, wait_until="networkidle", timeout=30000)

        items = page.query_selector_all(selectors["items"])
        results = []

        for item in items[:max_results]:
            try:
                title_el = item.query_selector(selectors["title"])
                price_el = item.query_selector(selectors["price"])
                link_el = item.query_selector(selectors.get("link", ""))
                image_el = item.query_selector(selectors.get("image", ""))

                title = title_el.inner_text().strip() if title_el else "N/A"
                price = price_el.inner_text().strip() if price_el else "N/A"
                link = link_el.get_attribute("href") if link_el else "N/A"
                image = image_el.get_attribute("src") if image_el else "N/A"

                if link and not link.startswith("http"):
                    link = config["base_url"] + link

                # Skip placeholder items
                if title == "N/A" or title == "" or "Shop on eBay" in title:
                    continue

                results.append({
                    "platform": platform,
                    "title": title,
                    "price": price,
                    "url": link,
                    "image_url": image,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                })
            except Exception:
                continue

        return results

    except Exception as e:
        print(f"Error scraping {platform}: {e}")
        return []


def scrape_all(query, platforms=None, max_results=5):
    """Scrape product listings from all specified platforms."""
    if platforms is None:
        platforms = list(PLATFORM_CONFIGS.keys())

    all_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()  # Use browser default User-Agent
        page = context.new_page()

        for platform in platforms:
            print(f"Searching {platform} for '{query}'...")
            results = scrape_platform(page, platform, query, max_results)
            all_results.extend(results)
            print(f"  Found {len(results)} results on {platform}")

        browser.close()

    return all_results


def format_results(results):
    """Format results as a readable comparison table."""
    if not results:
        return "No results found."

    output = []
    output.append(f"\n{'=' * 80}")
    output.append(f"  Price Comparison Results ({len(results)} items)")
    output.append(f"{'=' * 80}")

    for i, item in enumerate(results, 1):
        output.append(f"\n  #{i} [{item['platform'].upper()}]")
        output.append(f"  Title: {item['title'][:70]}")
        output.append(f"  Price: {item['price']}")
        output.append(f"  Link:  {item['url'][:80]}")
        output.append(f"  {'─' * 76}")

    output.append(f"\n{'=' * 80}\n")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Cross-Platform Price Scraper")
    parser.add_argument("--query", type=str, required=True, help="Product search query")
    parser.add_argument("--platforms", type=str, default=None,
                        help="Comma-separated platforms (amazon,ebay)")
    parser.add_argument("--max-results", type=int, default=5,
                        help="Max results per platform (default: 5)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output JSON file path")

    args = parser.parse_args()

    platforms = args.platforms.split(",") if args.platforms else None
    results = scrape_all(args.query, platforms, args.max_results)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {args.output}")
    else:
        print(format_results(results))


if __name__ == "__main__":
    main()
