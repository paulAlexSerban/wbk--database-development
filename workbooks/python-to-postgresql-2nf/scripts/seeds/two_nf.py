PRODUCTS_TABLE_SCHEMA = """
  CREATE TABLE products (
    sku VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0)
  )
"""

ORDER_ITEMS_TABLE_SCHEMA = """
  CREATE TABLE order_items (
    order_id INTEGER NOT NULL,
    product_sku VARCHAR(64) NOT NULL REFERENCES products(sku),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_sku)
  )
"""


def setup_two_nf_tables(conn):
    """Drop and recreate 2NF-compliant tables (FK-safe drop order)."""
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS order_items CASCADE")
            cur.execute("DROP TABLE IF EXISTS products CASCADE")
            cur.execute(PRODUCTS_TABLE_SCHEMA)
            cur.execute(ORDER_ITEMS_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating 2NF tables:", err)
        raise


def create_indexes(conn):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE INDEX idx_order_items_product_sku ON order_items (product_sku)"
            )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating indexes:", err)
        raise


def normalize_to_2nf(conn):
    """Transform order_items_1nf into 2NF tables.

    Removes partial dependencies: product_name and unit_price_cents move to
    products (keyed by sku). order_items keeps only quantity, which depends on
    the full composite key (order_id, product_sku).
    """
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT order_id, product_sku, product_name, unit_price_cents, quantity
                FROM order_items_1nf
                ORDER BY order_id, product_sku
                """
            )
            rows = cur.fetchall()

            seen_skus = set()

            for order_id, product_sku, product_name, unit_price_cents, quantity in rows:
                if product_sku not in seen_skus:
                    cur.execute(
                        """
                        INSERT INTO products (sku, name, unit_price_cents)
                        VALUES (%s, %s, %s)
                        """,
                        (product_sku, product_name, unit_price_cents),
                    )
                    seen_skus.add(product_sku)

                cur.execute(
                    """
                    INSERT INTO order_items (order_id, product_sku, quantity)
                    VALUES (%s, %s, %s)
                    """,
                    (order_id, product_sku, quantity),
                )

        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error normalizing to 2NF:", err)
        raise


def count_products(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*)::int AS count FROM products")
        return cur.fetchone()[0]


def count_order_items(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*)::int AS count FROM order_items")
        return cur.fetchone()[0]
