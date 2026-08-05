# Python to PostgreSQL 1NF

## Overview

This workbook demonstrates how to normalize data in a PostgreSQL database using Python.

## Setup

1. Clone the repository
2. Run `make compose_up` to start the containers
3. Run `make seed` to seed the database
4. Run `make compose_down` to stop the containers

## What it demonstrates
1. Before (violates 1NF): orders_unnormalized with delimited customer_phone_numbers and line_items
2. Migration: normalize_orders() splits those strings into atomic rows
3. After (1NF): customers, customer_phone_numbers, orders, order_items

## Verified
Stack is up; seed produced:
- 50 unnormalized orders → 50 customers, 111 phone numbers, 50 orders, 127 order items
- Delimited phones/line items correctly expanded (e.g. Catherine Owens → 3 phone rows; order totals via SUM)