# eBay Listing Strategy Reference

## Core Rule 1: Research Sold Listings Before Pricing

Before setting any price, search eBay for sold listings using the "Sold Items" filter.

- Use exact model numbers, not generic terms
- Note condition, included accessories, and shipping method
- Price ranges are more important than single data points
- Only sold data reflects true market value — never rely on active/unsold listings

## Core Rule 2: Title Optimization

eBay titles have an 80-character limit. Every character counts for search visibility.

### Title Format

```
[Brand] [Model] [Specifications] [Condition] [Key Feature] [Accessories]
```

### Title Rules

- Place the most searchable keywords first
- Never use filler words (WOW, L@@K, AMAZING, etc.)
- Include model numbers, not just product names
- Note color and size if applicable
- Use standard abbreviations only (NIB = New In Box, NWT = New With Tags)

### Title Examples

**Good:**
```
Apple iPhone 15 Pro Max 256GB Natural Titanium Unlocked A2849 w/ AppleCare+
```

**Bad:**
```
WOW!! Amazing iPhone BEST DEAL L@@K Must See!! Phone For Sale CHEAP!!!
```

## Core Rule 3: Fee Calculation

### Final Value Fee by Category

| Category | Final Value Fee |
|----------|----------------|
| Most categories | 13.25% |
| Clothing & Accessories | 12% |
| Guitars & Basses | 6% |
| Heavy Equipment | 3% |
| Books, DVDs, Music | 14.6% |

### Additional Fees

- Per-order fee: $0.30
- Payment processing (managed payments): ~2.9% + $0.30
- International fee: additional 1.65% (if applicable)
- Promoted listings: variable (2-20% of sale price)

### Quick Profit Estimation

Deduct **15-17%** from the final sale price for a rough net estimate. For more accuracy, use the `scripts/fee_calculator.py` script.

### Formula

```
Net Profit = Sale Price - (Sale Price × FVF%) - $0.30 - (Sale Price × 2.9%) - $0.30 - Item Cost - Shipping Cost
```

## Core Rule 4: Auction vs Buy It Now (BIN)

### Use Auction When

- Item is rare or collectible
- Market value is uncertain
- Time-sensitive selling (holidays, events)
- Building seller reputation (new account)
- Item has strong demand with competitive bidding potential

### Use Buy It Now When

- Market price is well-established
- Item is common with stable supply
- Price guarantee is needed
- High-value items (>$500) — avoids low-bid risk
- Steady inventory with consistent sales

### Hybrid Strategy

- Use "Buy It Now with Best Offer" for mid-range items ($50-$500)
- Set the BIN price 10-15% above target sale price
- Set minimum offer threshold at 70-80% of target

## Core Rule 5: Item Specifics & Description

### Item Specifics

- Fill in ALL available item specifics — they directly affect search ranking
- Use eBay's suggested values when possible
- Include: Brand, MPN, UPC/EAN, Condition, Color, Size, Material

### Description Best Practices

- Lead with key specifications
- List what is included (and explicitly what is NOT included)
- Note any defects or wear honestly — over-disclosure builds trust
- Include dimensions and weight
- Add compatibility information if applicable
- Use clean HTML formatting — avoid excessive styling or music/video embeds

## Core Rule 6: Seller-Side Scam Detection

Watch for these red flags from buyers:

| Red Flag | Risk | Action |
|----------|------|--------|
| Ship to address different from PayPal/payment address | Seller protection void | Only ship to verified address |
| "Can you end the listing early for $X?" | Likely scam to avoid eBay protections | Decline, let auction run |
| Overpayment + request to wire back difference | Fake payment / money laundering | Never refund overpayment via wire |
| Pressure for tracking before payment clears | "Item Not Received" claim | Wait for funds to clear |
| New account + freight forwarder address | Reshipping scam | Proceed with extreme caution |
| Buyer requests to communicate off-platform | Avoids eBay dispute resolution | Keep all communication on eBay |

## Core Rule 7: Buyer-Side Scam Detection

Watch for these red flags from sellers:

| Red Flag | Risk |
|----------|------|
| Price >50% below market | Likely counterfeit or non-delivery |
| Only stock photos, no actual item photos | May not have the item |
| Shipping country doesn't match listing claim | Counterfeit or long delivery |
| No returns + vague description | Hiding defects |
| Low feedback score with high-value items | Account may be compromised |
| Requests payment outside eBay | No buyer protection |

## Core Rule 8: Return Policy Impact

| Policy | Search Ranking | Conversion | Risk |
|--------|---------------|------------|------|
| 30-day free returns | Highest | Highest | Low (rarely used) |
| 30-day buyer-pays returns | Medium | Medium | Very Low |
| No returns | Lowest | Lowest | Medium (buyer can still file INAD) |
| Restocking fee | Medium | Lower | Low |

**Recommendation:** Offer 30-day free returns for most items. Despite seeming risky, return rates are typically under 5%, and the search ranking boost significantly increases sales volume.
