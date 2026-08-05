import sys

from scripts.db import get_connection
from scripts.seeds.one_nf import (
    ORDER_ITEMS_1NF,
    count_distinct_skus_1nf,
    count_order_items_1nf,
    insert_order_items_1nf,
    setup_order_items_1nf_table,
)
from scripts.seeds.two_nf import (
    count_order_items,
    count_products,
    create_indexes,
    normalize_to_2nf,
    setup_two_nf_tables,
)


def seed_one_nf():
    conn = get_connection()
    try:
        setup_order_items_1nf_table(conn)
        insert_order_items_1nf(conn, ORDER_ITEMS_1NF)
        count = count_order_items_1nf(conn)
        distinct_skus = count_distinct_skus_1nf(conn)
        print(
            f"Seeded {count} order_items_1nf rows "
            f"({distinct_skus} distinct product SKUs — product attrs repeated)"
        )
    finally:
        conn.close()


def seed_two_nf():
    conn = get_connection()
    try:
        setup_two_nf_tables(conn)
        normalize_to_2nf(conn)
        create_indexes(conn)
        print("Normalized into 2NF:")
        print(f"  {count_products(conn)} products")
        print(f"  {count_order_items(conn)} order items")
    finally:
        conn.close()


def seed():
    seed_one_nf()
    seed_two_nf()


if __name__ == "__main__":
    try:
        seed()
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)
