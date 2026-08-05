import string

from faker import Faker

fake = Faker()
_ALPHANUMERIC = string.ascii_letters + string.digits

PRODUCTS_2NF_TABLE_SCHEMA = """
  CREATE TABLE products_2nf (
    sku VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0),
    supplier_id INTEGER NOT NULL,
    supplier_name VARCHAR(255) NOT NULL,
    supplier_city VARCHAR(255) NOT NULL
  )
"""


def _random_sku(length=8):
    return "".join(fake.random_choices(elements=_ALPHANUMERIC, length=length))


def generate_supplier_catalog(count):
    """Small supplier catalog reused across many products (shows transitive redundancy)."""
    catalog = []
    for supplier_id in range(1, count + 1):
        catalog.append(
            {
                "supplier_id": supplier_id,
                "supplier_name": fake.company(),
                "supplier_city": fake.city(),
            }
        )
    return catalog


def generate_products_2nf(product_count, suppliers):
    """Generate 2NF products that violate 3NF via transitive dependencies.

    supplier_name and supplier_city depend on supplier_id, not on sku
    (sku → supplier_id → supplier_*).
    """
    rows = []
    seen_skus = set()
    while len(rows) < product_count:
        sku = _random_sku()
        if sku in seen_skus:
            continue
        seen_skus.add(sku)
        supplier = fake.random_element(elements=suppliers)
        rows.append(
            {
                "sku": sku,
                "name": fake.catch_phrase(),
                "unit_price_cents": fake.random_int(min=100, max=10000),
                "supplier_id": supplier["supplier_id"],
                "supplier_name": supplier["supplier_name"],
                "supplier_city": supplier["supplier_city"],
            }
        )
    return rows


SUPPLIER_CATALOG = generate_supplier_catalog(5)
PRODUCTS_2NF = generate_products_2nf(50, SUPPLIER_CATALOG)


def setup_products_2nf_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS products_2nf CASCADE")
            cur.execute(PRODUCTS_2NF_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating products_2nf table:", err)
        raise


def insert_products_2nf(conn, products):
    try:
        with conn.cursor() as cur:
            for product in products:
                cur.execute(
                    """
                    INSERT INTO products_2nf
                      (sku, name, unit_price_cents, supplier_id, supplier_name, supplier_city)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        product["sku"],
                        product["name"],
                        product["unit_price_cents"],
                        product["supplier_id"],
                        product["supplier_name"],
                        product["supplier_city"],
                    ),
                )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error inserting products_2nf:", err)
        raise


def count_products_2nf(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*)::int AS count FROM products_2nf")
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting products_2nf:", err)
        raise


def count_distinct_suppliers_2nf(conn):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(DISTINCT supplier_id)::int AS count FROM products_2nf"
            )
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting distinct suppliers:", err)
        raise
