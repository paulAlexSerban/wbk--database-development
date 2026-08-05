import string

from faker import Faker

fake = Faker()
_ALPHANUMERIC = string.ascii_letters + string.digits

ORDER_ITEMS_1NF_TABLE_SCHEMA = """
  CREATE TABLE order_items_1nf (
    order_id INTEGER NOT NULL,
    product_sku VARCHAR(64) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_sku)
  )
"""


def _random_sku(length=8):
    return "".join(fake.random_choices(elements=_ALPHANUMERIC, length=length))


def generate_product_catalog(count):
    """Small product catalog reused across many order lines (shows redundancy)."""
    catalog = []
    for _ in range(count):
        catalog.append(
            {
                "product_sku": _random_sku(),
                "product_name": fake.catch_phrase(),
                "unit_price_cents": fake.random_int(min=100, max=10000),
            }
        )
    return catalog


def generate_order_items_1nf(order_count, catalog, items_per_order_max=3):
    """Generate 1NF order lines that violate 2NF via partial dependencies.

    product_name and unit_price_cents depend only on product_sku, not the full
    composite key (order_id, product_sku).
    """
    rows = []
    for order_id in range(1, order_count + 1):
        item_count = fake.random_int(min=1, max=min(items_per_order_max, len(catalog)))
        chosen = fake.random_elements(
            elements=catalog, length=item_count, unique=True
        )
        for product in chosen:
            rows.append(
                {
                    "order_id": order_id,
                    "product_sku": product["product_sku"],
                    "product_name": product["product_name"],
                    "unit_price_cents": product["unit_price_cents"],
                    "quantity": fake.random_int(min=1, max=10),
                }
            )
    return rows


PRODUCT_CATALOG = generate_product_catalog(10)
ORDER_ITEMS_1NF = generate_order_items_1nf(50, PRODUCT_CATALOG)


def setup_order_items_1nf_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS order_items_1nf CASCADE")
            cur.execute(ORDER_ITEMS_1NF_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating order_items_1nf table:", err)
        raise


def insert_order_items_1nf(conn, order_items):
    try:
        with conn.cursor() as cur:
            for item in order_items:
                cur.execute(
                    """
                    INSERT INTO order_items_1nf
                      (order_id, product_sku, product_name, unit_price_cents, quantity)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        item["order_id"],
                        item["product_sku"],
                        item["product_name"],
                        item["unit_price_cents"],
                        item["quantity"],
                    ),
                )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error inserting order_items_1nf:", err)
        raise


def count_order_items_1nf(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*)::int AS count FROM order_items_1nf")
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting order_items_1nf:", err)
        raise


def count_distinct_skus_1nf(conn):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(DISTINCT product_sku)::int AS count FROM order_items_1nf"
            )
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting distinct SKUs:", err)
        raise
