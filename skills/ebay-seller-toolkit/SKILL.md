---
name: ebay-seller-toolkit
description: >
  This skill should be used when the user needs help with eBay selling, buying,
  or flipping items. It covers listing optimization, pricing strategy research,
  shipping calculation, fee estimation, scam detection, trading card analysis,
  cross-platform price comparison, and ecommerce data collection. Trigger phrases
  include "eBay", "listing", "eBay pricing", "eBay shipping", "trading card",
  "price compare", "ecommerce scrape", "eBay fees", "eBay scam", "卖货",
  "刊登", "定价", "发货", "比价", "采集", "交易卡", "跨平台".
---

# eBay Seller Toolkit

A comprehensive eBay seller toolkit covering listing optimization, pricing research, shipping strategy, fee calculation, scam detection, trading card analysis, cross-platform price comparison, and ecommerce product data collection.

## When to Use

Invoke this skill when the user's request involves any of the following:

- Creating, optimizing, or managing eBay listings
- Researching pricing or fee structures on eBay
- Planning shipping strategies or calculating shipping costs
- Detecting buyer/seller scams on eBay
- Analyzing trading cards (sports cards, Pokémon, etc.) for eBay listing
- Comparing prices across multiple ecommerce platforms (Amazon, eBay, AliExpress, Temu, JD, Taobao, etc.)
- Collecting product data from ecommerce websites (via official APIs or compliant methods)
- Multi-SKU management, competitive analysis, or fulfillment planning

## Core Capabilities

This skill integrates **five** major capability modules. Each module has detailed reference documentation in the `references/` directory.

### Module 1: eBay Listing & Selling (Core)

The foundational module for eBay sellers. Covers end-to-end selling workflow.

**Key areas:**
- **Title optimization** — 80-char limit, format: `[Brand] [Model] [Specs] [Condition] [Key Feature] [Accessories]`
- **Fee calculation** — Final Value Fee (13.25% most categories, 12% clothing, 6% guitars, 3% heavy equipment) + $0.30/order + ~2.9% payment processing. Quick estimate: deduct 15-17% from sale price.
- **Auction vs Buy It Now** — Use auction for rare/collectible items with uncertain value; use BIN for common items with known market price or high-value items (>$500).
- **Return policy** — 30-day free returns recommended (boosts search ranking, rarely used by buyers).
- **Scam detection** — Both buyer-side and seller-side red flags.

> For full rules and details, read `references/listing.md`.

### Module 2: Pricing Strategy & Research

Research-driven pricing using sold listing data.

**Key areas:**
- Always search eBay "Sold Items" filter before pricing
- Use exact model numbers, not generic terms
- Price ranges matter more than single data points
- Account for condition, included accessories, and shipping method
- Never price based on unsold/active listings — only sold data reflects true market value

> For full pricing methodology, read `references/pricing.md`.

### Module 3: Shipping & Fulfillment

Shipping strategy optimization for cost and conversion rate.

**Key areas:**
- Free shipping converts better but must factor cost into item price
- Calculated shipping is better for heavy/oversized items
- Always add 1-day handling buffer
- Pack items before listing to know exact dimensions and weight
- Signature confirmation required for items over $750

> For full shipping guide, read `references/shipping.md`.

### Module 4: Trading Card Analysis & Listing

Specialized module for trading card sellers (sports cards, Pokémon, etc.).

**Key areas:**
- Card condition analysis and grading estimation from photos
- Title and description optimization for card listings
- Market intelligence: trending cards, recent sold data, price prediction
- Grading ROI calculator (PSA vs BGS vs SGC comparison)
- Cross-platform price comparison (eBay, COMC, PWCC)
- Seasonal trend prediction and portfolio optimization

> For full trading card guide, read `references/trading-cards.md`.

### Module 5: Cross-Platform Price Comparison & Data Collection

Tools for price hunting and ecommerce data collection.

**Key areas:**
- **Price comparison** across Amazon, eBay, AliExpress, Temu, Walmart, JD, Taobao, Tmall, PDD, Rakuten, Coupang, Shopee
- Structured output: platform, price (currency-normalized), seller rating, shipping estimate, direct link
- Purchase recommendations: best value, fastest delivery, most reliable seller
- **Ecommerce data collection** using official APIs and compliant web scraping with Playwright
- Batch product data collection (title, price, store, link, image, timestamp)
- Mandatory robots.txt compliance and rate limiting

> For price comparison workflow, read `references/price-comparison.md`.
> For data collection guide, read `references/scraping-guide.md`.

### Module 6: Shipping Label & Logistics Management

Shipping rate comparison, label purchasing, and package tracking across carriers.

**Key areas:**
- **Rate comparison** — Real-time rate lookup across USPS, FedEx, and UPS for any origin/destination/weight
- **Label purchasing** — Buy discounted shipping labels with AI-assisted address collection; supports PDF, PNG, and ZPL formats
- **Package tracking** — Real-time tracking status, ETA, and full event timeline by tracking number
- **Address validation** — Verify delivery addresses before purchasing labels to avoid surcharges
- **Additional services** — Signature confirmation, insurance, reference numbers
- **Label management** — View, void (within carrier window), and reprint historical labels
- **Safety rule**: Never auto-purchase labels without explicit user confirmation of carrier, service, price, and address

> For full logistics guide, read `references/shipping-logistics.md`.

### Module 7: Multi-Platform Seller Comparison & Decision

Helping sellers choose where and how to sell across multiple marketplaces.

**Key areas:**
- **Platform fee comparison** — Detailed fee breakdown for Amazon (8-45% referral + FBA + storage), eBay (category-specific FVF), Walmart (8-15%), Poshmark (~20%), Mercari, FB Marketplace
- **True cost calculation** — Factor in platform fees + shipping + taxes + return costs (15-30% return rate in some categories)
- **Pricing based on sold data** — Only use completed/sold listings, never active listings, to determine market value
- **Account health & risk** — Amazon ODR >1% = account death; review manipulation = permanent ban; IP complaints = immediate suspension
- **Scam detection by platform** — Platform-specific fraud patterns (stock photos on local markets, triangle scams, off-platform payment requests)
- **Role-based guidance** — Buyer (price compare, negotiate), Seller (listing, pricing, rules), Arbitrage (ROI, ToS risks), Compliance (tax, legal)

> For full marketplace decision guide, read `references/marketplace-decision.md`.

### Module 8: Cross-Border Ecommerce Tools

Comprehensive cross-border selling toolkit spanning multiple platforms and data sources.

**Key areas:**
- **Multi-platform product research** — Search and analyze products across Amazon, TikTok Shop, eBay, Walmart, and 1688 (sourcing)
- **Keyword & traffic analysis** — Reverse ASIN keyword lookup, traffic source analysis, keyword competition density
- **Competitor deep analysis** — Batch ASIN detail queries, A+ content analysis, review mining and sentiment breakdown
- **Patent & IP risk detection** — Design patent, invention patent, trademark, and copyright checks before listing (important for cross-border sellers)
- **Market trend intelligence** — Google Trends integration, trending products, seasonal pattern identification
- **AI-assisted content** — Product image analysis, title keyword extraction, smart categorization
- **1688 sourcing** — Search Chinese supplier catalogs, compare MOQ, price tiers, and supplier ratings

> For full cross-border tools guide, read `references/cross-border-tools.md`.

### Module 9: Global Multi-Site Price Scanning

Scan the same product across different eBay country sites and global ecommerce sites to identify regional price differences.

**Key areas:**
- **eBay multi-site scanning** — Compare prices for the same item across ebay.com, ebay.co.uk, ebay.de, ebay.fr, ebay.com.au, ebay.ca, ebay.it, ebay.es, etc.
- **Currency normalization** — Convert all prices to a single base currency (user's choice) for fair comparison
- **Regional arbitrage detection** — Identify items significantly cheaper on one country site vs another
- **Tax & import duty awareness** — Flag potential customs/VAT implications when buying cross-border
- **Structured comparison output** — Table format with country site, local price, converted price, shipping estimate, seller rating
- **Best deal recommendation** — Factor in price + shipping + import costs to recommend the true cheapest source

> For full global price scanning guide, read `references/global-price-scan.md`.

## Workflow

When helping a user with eBay-related tasks, follow this general approach:

1. **Identify the task type** — Determine which module(s) apply to the user's request.
2. **Load relevant references** — Read the appropriate `references/` files for detailed procedures.
3. **Research first** — Before suggesting prices, always check sold listings data. Before creating listings, understand the product and competition.
4. **Apply best practices** — Follow the core rules for titles, fees, shipping, and scam avoidance.
5. **Generate actionable output** — Provide optimized titles, calculated fees, shipping recommendations, or structured price comparison tables as appropriate.

## Scripts

- `scripts/fee_calculator.py` — Calculate eBay fees and estimate net profit for a given sale price and category.
- `scripts/price_scraper.py` — Collect and compare prices across multiple ecommerce platforms for a given product.

## Common Pitfalls to Avoid

1. **Underestimating shipping** — Weigh and measure before listing; heavy items lose money with free shipping.
2. **Ignoring item specifics** — Listings without specs get buried in search results.
3. **Pricing from active listings** — Unsold listings do not reflect market value; always filter by "Sold Items".
4. **Shipping before payment clears** — Risk "Item Not Received" claims; wait for funds to clear.
5. **Accepting unverified payment** — For items >$750, require signature confirmation.
