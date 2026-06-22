# Shipping Label & Logistics Management Reference

## Overview

Compare shipping rates across carriers, purchase discounted labels, track packages, and manage logistics. Integrates USPS, FedEx, and UPS.

## Carrier Comparison

| Carrier | Services | Best For |
|---------|----------|----------|
| USPS | First Class, Priority Mail, Priority Flat Rate, Express | Items under 5 lbs |
| FedEx | Ground, Express Saver, 2Day, Overnight | 5-50 lb, time-sensitive |
| UPS | Ground, 2nd Day Air, Next Day Air | Heavy items, business addresses |

### Rate Lookup Requirements

- Origin ZIP/city, Destination ZIP/city, Weight (oz/lb/g/kg), Dimensions (optional)
- Query all carriers, sort by price, show delivery time and service level

## Label Purchase Flow

1. User selects carrier and service
2. Collect complete sender and recipient addresses
3. **MANDATORY**: Display carrier, service, price, and full addresses for user confirmation
4. **NEVER auto-purchase** — wait for explicit user approval
5. Process payment and generate label (PDF, PNG, or ZPL format)

### Additional Services

| Service | When to Use |
|---------|-------------|
| Signature Confirmation | Items >$750 (required for eBay seller protection) |
| Insurance | Items >$100, fragile items |
| Reference Number | Link label to order ID for tracking |

### Label Management

- **View**: List all purchased labels with status
- **Void**: Cancel within carrier window (USPS: 28 days, FedEx/UPS: 1 day)
- **Reprint**: Re-download any historical label

## Package Tracking

Provide tracking number to get:
- Current status (In Transit, Out for Delivery, Delivered, etc.)
- Current location
- Estimated delivery date (ETA)
- Full event timeline with timestamps

## Address Validation

Always validate addresses before label purchase to avoid:
- Surcharges for address corrections
- Delivery failures and returns
- Lost packages
