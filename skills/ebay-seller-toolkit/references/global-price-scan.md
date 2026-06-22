# Global Multi-Site Price Scanning Reference

## Overview

Scan the same product across different eBay country sites and global ecommerce platforms to find regional price differences and cross-border arbitrage opportunities.

## Supported eBay Country Sites

| Site | URL | Currency |
|------|-----|----------|
| US | ebay.com | USD |
| UK | ebay.co.uk | GBP |
| Germany | ebay.de | EUR |
| France | ebay.fr | EUR |
| Australia | ebay.com.au | AUD |
| Canada | ebay.ca | CAD |
| Italy | ebay.it | EUR |
| Spain | ebay.es | EUR |
| Japan | ebay.co.jp | JPY |

## Price Scanning Workflow

### Step 1: Identify the Product

Collect exact product identifier:
- Model number, brand + model name, or eBay item number
- Condition requirement (new, used, refurbished)

### Step 2: Search Across Sites

For each country site:
1. Search using the same product keywords (translate if needed)
2. Extract: listing title, price (local currency), shipping cost, seller rating, item URL
3. Filter by condition and relevance

### Step 3: Currency Normalization

- Convert all prices to user's preferred base currency
- Show both local price and converted price
- Use current exchange rates (note rates are approximate)

### Step 4: Total Cost Calculation

For each result, calculate true landed cost:

```
Landed Cost = Item Price + Shipping to User's Country + Estimated Import Duty + Estimated VAT/Tax
```

### Step 5: Comparison Output

| # | Site | Local Price | USD Equiv. | Shipping | Est. Duty/Tax | Total Cost | Seller Rating |
|---|------|-------------|-----------|----------|---------------|------------|---------------|
| 1 | ebay.de | €85.00 | $92.50 | €12.00 | $8.00 | $113.50 | 99.5% |
| 2 | ebay.com | $119.99 | $119.99 | Free | $0 | $119.99 | 98.2% |
| 3 | ebay.co.uk | £78.00 | $98.50 | £8.00 | $10.00 | $118.60 | 99.1% |

### Step 6: Recommendation

Provide best option considering:
1. **Lowest total cost** (item + shipping + duties)
2. **Fastest delivery** (domestic vs international)
3. **Lowest risk** (seller rating + buyer protection)

## Regional Arbitrage Detection

Flag opportunities where:
- Same item is >20% cheaper on one country site vs another
- After accounting for shipping and duties, savings still exceed 10%
- Seller has strong ratings (>98%) on the cheaper site

## Important Considerations

- **Import duties & taxes**: Vary by country and product category; estimates only
- **Warranty**: Cross-border purchases may void local warranty
- **Returns**: International returns are more complex and costly
- **Electrical compatibility**: Voltage/plug differences for electronics
- **Currency fluctuation**: Exchange rates change; lock in price at purchase time
- **eBay Global Shipping Program**: Simplifies international buying but may add cost
