#!/usr/bin/env python3
"""
eBay Fee Calculator

Calculates eBay fees and estimates net profit for a given sale price and category.

Usage:
    python fee_calculator.py --price 100 --category general
    python fee_calculator.py --price 250 --category clothing --shipping 12.50 --cost 80
"""

import argparse
import json
import sys

# Final Value Fee rates by category
FVF_RATES = {
    "general": 0.1325,         # Most categories: 13.25%
    "clothing": 0.12,          # Clothing & Accessories: 12%
    "guitars": 0.06,           # Guitars & Basses: 6%
    "heavy_equipment": 0.03,   # Heavy Equipment: 3%
    "books_media": 0.146,      # Books, DVDs, Music: 14.6%
    "electronics": 0.1325,     # Consumer Electronics: 13.25%
    "collectibles": 0.1325,    # Collectibles: 13.25%
    "sports_cards": 0.1325,    # Sports Memorabilia & Cards: 13.25%
    "jewelry": 0.1325,         # Jewelry: 13.25% (up to $7500)
    "auto_parts": 0.1325,      # Auto Parts: 13.25%
}

PER_ORDER_FEE = 0.30           # $0.30 per order
PAYMENT_PROCESSING_RATE = 0.029  # 2.9% managed payments
PAYMENT_PROCESSING_FIXED = 0.30  # $0.30 per transaction
INTERNATIONAL_FEE_RATE = 0.0165  # 1.65% for international sales


def calculate_fees(sale_price, category="general", is_international=False, promoted_rate=0):
    """Calculate eBay fees for a given sale price and category."""
    fvf_rate = FVF_RATES.get(category, FVF_RATES["general"])

    # Final Value Fee
    final_value_fee = sale_price * fvf_rate

    # Per-order fee
    per_order = PER_ORDER_FEE

    # Payment processing
    payment_processing = sale_price * PAYMENT_PROCESSING_RATE + PAYMENT_PROCESSING_FIXED

    # International fee (if applicable)
    international_fee = sale_price * INTERNATIONAL_FEE_RATE if is_international else 0

    # Promoted listing fee (if applicable)
    promoted_fee = sale_price * (promoted_rate / 100) if promoted_rate > 0 else 0

    # Total fees
    total_fees = final_value_fee + per_order + payment_processing + international_fee + promoted_fee

    return {
        "sale_price": round(sale_price, 2),
        "final_value_fee": round(final_value_fee, 2),
        "fvf_rate": f"{fvf_rate * 100}%",
        "per_order_fee": round(per_order, 2),
        "payment_processing": round(payment_processing, 2),
        "international_fee": round(international_fee, 2),
        "promoted_fee": round(promoted_fee, 2),
        "total_fees": round(total_fees, 2),
        "fee_percentage": f"{round(total_fees / sale_price * 100, 1)}%",
        "after_fees": round(sale_price - total_fees, 2),
    }


def calculate_profit(sale_price, item_cost=0, shipping_cost=0, category="general",
                     is_international=False, promoted_rate=0):
    """Calculate net profit after all fees and costs."""
    fees = calculate_fees(sale_price, category, is_international, promoted_rate)

    net_profit = fees["after_fees"] - item_cost - shipping_cost
    roi = (net_profit / item_cost * 100) if item_cost > 0 else 0

    return {
        **fees,
        "item_cost": round(item_cost, 2),
        "shipping_cost": round(shipping_cost, 2),
        "net_profit": round(net_profit, 2),
        "roi": f"{round(roi, 1)}%",
    }


def main():
    parser = argparse.ArgumentParser(description="eBay Fee Calculator")
    parser.add_argument("--price", type=float, required=True, help="Sale price in USD")
    parser.add_argument("--category", type=str, default="general",
                        choices=list(FVF_RATES.keys()),
                        help="Product category (default: general)")
    parser.add_argument("--cost", type=float, default=0, help="Item cost/purchase price")
    parser.add_argument("--shipping", type=float, default=0, help="Shipping cost")
    parser.add_argument("--international", action="store_true", help="International sale")
    parser.add_argument("--promoted", type=float, default=0, help="Promoted listing rate (%%)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    result = calculate_profit(
        sale_price=args.price,
        item_cost=args.cost,
        shipping_cost=args.shipping,
        category=args.category,
        is_international=args.international,
        promoted_rate=args.promoted,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"\n{'=' * 50}")
        print(f"  eBay Fee Calculator")
        print(f"{'=' * 50}")
        print(f"  Sale Price:           ${result['sale_price']:.2f}")
        print(f"  Category:             {args.category} ({result['fvf_rate']})")
        print(f"{'─' * 50}")
        print(f"  Final Value Fee:      -${result['final_value_fee']:.2f}")
        print(f"  Per-Order Fee:        -${result['per_order_fee']:.2f}")
        print(f"  Payment Processing:   -${result['payment_processing']:.2f}")
        if result['international_fee'] > 0:
            print(f"  International Fee:    -${result['international_fee']:.2f}")
        if result['promoted_fee'] > 0:
            print(f"  Promoted Listing Fee: -${result['promoted_fee']:.2f}")
        print(f"{'─' * 50}")
        print(f"  Total Fees:           -${result['total_fees']:.2f} ({result['fee_percentage']})")
        print(f"  After Fees:           ${result['after_fees']:.2f}")
        if args.cost > 0 or args.shipping > 0:
            print(f"{'─' * 50}")
            print(f"  Item Cost:            -${result['item_cost']:.2f}")
            print(f"  Shipping Cost:        -${result['shipping_cost']:.2f}")
            print(f"  Net Profit:           ${result['net_profit']:.2f}")
            print(f"  ROI:                  {result['roi']}")
        print(f"{'=' * 50}\n")


if __name__ == "__main__":
    main()
