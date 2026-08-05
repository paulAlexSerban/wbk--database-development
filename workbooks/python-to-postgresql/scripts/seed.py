import sys

from scripts.db import get_connection
from scripts.seeds.users import (
    USERS,
    count_users,
    insert_users,
    setup_users_table,
)
from scripts.seeds.customer_orders import (
    CUSTOMERS,
    ORDER_ITEMS,
    ORDERS,
    count_customers,
    count_order_items,
    count_orders,
    create_indexes,
    insert_customers,
    insert_order_items,
    insert_orders,
    join_across_all_tables,
    setup_customers_table,
    setup_order_items_table,
    setup_orders_table,
)


def seed_users():
    conn = get_connection()
    try:
        setup_users_table(conn)
        insert_users(conn, USERS)
        count = count_users(conn)
        print(f"Seeded {count} users")
    finally:
        conn.close()


def seed_customers():
    conn = get_connection()
    try:
        setup_customers_table(conn)
        insert_customers(conn, CUSTOMERS)
        count = count_customers(conn)
        print(f"Seeded {count} customers")
    finally:
        conn.close()


def seed_orders():
    conn = get_connection()
    try:
        setup_orders_table(conn)
        insert_orders(conn, ORDERS)
        count = count_orders(conn)
        print(f"Seeded {count} orders")
    finally:
        conn.close()


def seed_order_items():
    conn = get_connection()
    try:
        setup_order_items_table(conn)
        insert_order_items(conn, ORDER_ITEMS)
        count = count_order_items(conn)
        print(f"Seeded {count} order items")
        create_indexes(conn)
        rows = join_across_all_tables(conn)
        print(rows)
    finally:
        conn.close()


def seed():
    seed_users()
    seed_customers()
    seed_orders()
    seed_order_items()


if __name__ == "__main__":
    try:
        seed()
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)
