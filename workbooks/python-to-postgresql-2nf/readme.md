# Python to PostgreSQL 2NF

## Overview

This workbook demonstrates Second Normal Form (2NF) normalization in PostgreSQL using Python.

## Setup

1. Clone the repository
2. Run `make compose_up` to start the containers
3. Run `make seed` to seed the database
4. Run `make compose_down` to stop the containers

## What it demonstrates
1. Before (1NF, violates 2NF): `order_items_1nf` with composite PK `(order_id, product_sku)` where `product_name` and `unit_price_cents` depend only on `product_sku` (partial dependency)
2. Migration: `normalize_to_2nf()` moves product attributes into a `products` table
3. After (2NF): `products` + `order_items` (line items keep only attributes that depend on the full key)

## Verified
Stack is up; seed produced:
- ~100 order_items_1nf rows with 10 distinct product SKUs (product name/price repeated across lines)
- Normalized to 10 products + matching order_items rows
- Product rename updates one `products` row instead of many line-item rows
