import sys

from scripts.db import get_connection
from scripts.seeds.two_nf import (
    PRODUCTS_2NF,
    count_distinct_suppliers_2nf,
    count_products_2nf,
    insert_products_2nf,
    setup_products_2nf_table,
)
from scripts.seeds.three_nf import (
    count_products,
    count_suppliers,
    create_indexes,
    normalize_to_3nf,
    setup_three_nf_tables,
)


def seed_two_nf():
    conn = get_connection()
    try:
        setup_products_2nf_table(conn)
        insert_products_2nf(conn, PRODUCTS_2NF)
        count = count_products_2nf(conn)
        distinct_suppliers = count_distinct_suppliers_2nf(conn)
        print(
            f"Seeded {count} products_2nf rows "
            f"({distinct_suppliers} distinct suppliers — supplier attrs repeated)"
        )
    finally:
        conn.close()


def seed_three_nf():
    conn = get_connection()
    try:
        setup_three_nf_tables(conn)
        normalize_to_3nf(conn)
        create_indexes(conn)
        print("Normalized into 3NF:")
        print(f"  {count_suppliers(conn)} suppliers")
        print(f"  {count_products(conn)} products")
    finally:
        conn.close()


def seed():
    seed_two_nf()
    seed_three_nf()


if __name__ == "__main__":
    try:
        seed()
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)
