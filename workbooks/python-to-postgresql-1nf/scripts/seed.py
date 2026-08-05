import sys

from scripts.db import get_connection
from scripts.seeds.unnormalized import (
    UNNORMALIZED_ORDERS,
    count_unnormalized_orders,
    insert_unnormalized_orders,
    setup_orders_unnormalized_table,
)
from scripts.seeds.normalized import (
    count_customer_phone_numbers,
    count_customers,
    count_order_items,
    count_orders,
    create_indexes,
    normalize_orders,
    setup_normalized_tables,
)


def seed_unnormalized():
    conn = get_connection()
    try:
        setup_orders_unnormalized_table(conn)
        insert_unnormalized_orders(conn, UNNORMALIZED_ORDERS)
        count = count_unnormalized_orders(conn)
        print(f"Seeded {count} unnormalized orders")
    finally:
        conn.close()


def seed_normalized():
    conn = get_connection()
    try:
        setup_normalized_tables(conn)
        normalize_orders(conn)
        create_indexes(conn)
        print(f"Normalized into:")
        print(f"  {count_customers(conn)} customers")
        print(f"  {count_customer_phone_numbers(conn)} customer phone numbers")
        print(f"  {count_orders(conn)} orders")
        print(f"  {count_order_items(conn)} order items")
    finally:
        conn.close()


def seed():
    seed_unnormalized()
    seed_normalized()


if __name__ == "__main__":
    try:
        seed()
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)
