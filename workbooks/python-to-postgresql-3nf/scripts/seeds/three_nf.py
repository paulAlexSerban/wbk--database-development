SUPPLIERS_TABLE_SCHEMA = """
  CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL
  )
"""

PRODUCTS_TABLE_SCHEMA = """
  CREATE TABLE products (
    sku VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id)
  )
"""


def setup_three_nf_tables(conn):
    """Drop and recreate 3NF-compliant tables (FK-safe drop order)."""
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS products CASCADE")
            cur.execute("DROP TABLE IF EXISTS suppliers CASCADE")
            cur.execute(SUPPLIERS_TABLE_SCHEMA)
            cur.execute(PRODUCTS_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating 3NF tables:", err)
        raise


def create_indexes(conn):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE INDEX idx_products_supplier_id ON products (supplier_id)"
            )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating indexes:", err)
        raise


def normalize_to_3nf(conn):
    """Transform products_2nf into 3NF tables.

    Removes transitive dependencies: supplier_name and supplier_city move to
    suppliers (keyed by id). products keeps only supplier_id.
    """
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT sku, name, unit_price_cents,
                       supplier_id, supplier_name, supplier_city
                FROM products_2nf
                ORDER BY sku
                """
            )
            rows = cur.fetchall()

            seen_supplier_ids = set()

            for (
                sku,
                name,
                unit_price_cents,
                supplier_id,
                supplier_name,
                supplier_city,
            ) in rows:
                if supplier_id not in seen_supplier_ids:
                    cur.execute(
                        """
                        INSERT INTO suppliers (id, name, city)
                        VALUES (%s, %s, %s)
                        """,
                        (supplier_id, supplier_name, supplier_city),
                    )
                    seen_supplier_ids.add(supplier_id)

                cur.execute(
                    """
                    INSERT INTO products (sku, name, unit_price_cents, supplier_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (sku, name, unit_price_cents, supplier_id),
                )

        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error normalizing to 3NF:", err)
        raise


def count_suppliers(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*)::int AS count FROM suppliers")
        return cur.fetchone()[0]


def count_products(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*)::int AS count FROM products")
        return cur.fetchone()[0]
