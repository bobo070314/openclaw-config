# Cross-Platform Price Comparison Reference

## Supported Platforms

### International Platforms

| Platform | Region | URL Pattern | Notes |
|----------|--------|-------------|-------|
| Amazon | Global | amazon.com, amazon.co.uk, amazon.de, etc. | Multiple regional sites |
| eBay | Global | ebay.com, ebay.co.uk, ebay.de, etc. | Sold data available |
| AliExpress | Global (CN sellers) | aliexpress.com | Low prices, longer shipping |
| Temu | Global (CN sellers) | temu.com | Aggressive pricing, newer platform |
| Walmart | US | walmart.com | Competitive with Amazon |
| Rakuten | Japan | rakuten.co.jp | Japanese marketplace |
| Coupang | South Korea | coupang.com | Rocket delivery |
| Shopee | Southeast Asia | shopee.sg, shopee.co.th, etc. | Regional variants |

### China Domestic Platforms

| Platform | URL | Notes |
|----------|-----|-------|
| JD.com (京东) | jd.com | Fast delivery, reliable quality |
| Taobao (淘宝) | taobao.com | Largest C2C marketplace |
| Tmall (天猫) | tmall.com | B2C, brand-authorized stores |
| PDD (拼多多) | pinduoduo.com | Group buying, lowest prices |

## Price Comparison Workflow

### Step 1: Confirm Product Information

Before searching, clarify:
- Exact product name / model number
- Preferred currency (default: USD)
- Region preference (default: global)
- Condition requirement (new / used / refurbished)
- Special requirements (e.g., Prime shipping, local warehouse)

### Step 2: Execute Multi-Platform Search

Search across platforms in this priority order:
1. Amazon (largest catalog, reliable pricing)
2. eBay (check both active and sold listings)
3. AliExpress / Temu (China direct pricing)
4. Walmart (US competitive pricing)
5. Regional platforms as applicable (JD, Taobao, etc.)

### Step 3: Data Extraction

For each result, extract:
- Platform name
- Product title / listing title
- Price (in original currency)
- Price (converted to user's preferred currency)
- Seller name / store name
- Seller rating / feedback score
- Shipping cost estimate
- Estimated delivery time
- Direct product link
- Availability status

### Step 4: Currency Normalization

- Convert all prices to the user's preferred currency
- Use current exchange rates
- Include original currency price in parentheses
- Note if prices include/exclude tax and shipping

### Step 5: Generate Comparison Output

#### Table Format (for Markdown-capable platforms)

```markdown
| # | Platform | Price (USD) | Seller Rating | Shipping | Delivery | Link |
|---|----------|-------------|---------------|----------|----------|------|
| 1 | Amazon   | $29.99      | 4.5/5 ⭐      | Free     | 2 days   | [Link](url) |
| 2 | eBay     | $27.50      | 99.2%         | $4.99    | 3-5 days | [Link](url) |
| 3 | AliExpress| $18.99     | 95.3%         | Free     | 15-25 days| [Link](url) |
```

#### List Format (for Discord/WhatsApp/plain text)

```
🏆 Price Comparison: [Product Name]

1. Amazon — $29.99 (Free shipping, 2-day delivery) ⭐4.5/5
2. eBay — $27.50 + $4.99 shipping (3-5 days) ⭐99.2%
3. AliExpress — $18.99 (Free shipping, 15-25 days) ⭐95.3%
```

### Step 6: Purchase Recommendations

Provide recommendations across three dimensions:

1. **🏅 Best Value**: Lowest total cost (price + shipping + tax)
2. **🚀 Fastest Delivery**: Shortest delivery time with reliable tracking
3. **🛡️ Most Reliable**: Highest seller rating + best return policy + buyer protection

## Platform-Specific Search Tips

### Amazon
- Search by ASIN for exact match
- Check "Other Sellers" for price comparison within platform
- CamelCamelCamel for price history tracking

### eBay
- Use "Sold Items" filter for true market value
- Check "Buy It Now" and "Auction" separately
- International versions may be cheaper

### AliExpress / Temu
- Search in both English and Chinese for more results
- Check seller ratings and store age
- Read recent reviews for quality assessment
- Factor in 15-45 day shipping times

### JD / Taobao / PDD
- Prices often shown in CNY — convert to user currency
- JD: Look for 自营 (self-operated) for quality guarantee
- Taobao: Check 天猫 (Tmall) stores for B2C guarantee
- PDD: Verify 百亿补贴 (Billion Subsidy) items for authentic deals

## Limitations & Disclaimers

- Prices change frequently; search results are point-in-time snapshots
- Some platforms require login for full pricing (Taobao, JD)
- PDD app links cannot be directly generated — provide search keywords instead
- International shipping costs and import duties may apply
- Currency conversions are approximate based on current rates
- Always verify final price on the platform before purchasing
