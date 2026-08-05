# Python to PostgreSQL 3NF

## Overview

This workbook demonstrates Third Normal Form (3NF) normalization in PostgreSQL using Python.

## Setup

1. Clone the repository
2. Run `make compose_up` to start the containers
3. Run `make seed` to seed the database
4. Run `make compose_down` to stop the containers

## What it demonstrates
1. Before (2NF, violates 3NF): `products_2nf` where `supplier_name` and `supplier_city` depend on `supplier_id`, not on the product key `sku` (transitive dependency)
2. Migration: `normalize_to_3nf()` moves supplier attributes into a `suppliers` table
3. After (3NF): `suppliers` + `products` (products keep only a `supplier_id` foreign key)

## Verified
Stack is up; seed produced:
- 50 products_2nf rows with 5 distinct suppliers (supplier name/city repeated across products)
- Normalized to 5 suppliers + 50 products
- Supplier city update touches one `suppliers` row instead of many product rows
