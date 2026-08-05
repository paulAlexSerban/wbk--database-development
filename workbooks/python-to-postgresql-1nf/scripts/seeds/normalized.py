CUSTOMERS_TABLE_SCHEMA = """
  CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
  )
"""

CUSTOMER_PHONE_NUMBERS_TABLE_SCHEMA = """
  CREATE TABLE customer_phone_numbers (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    phone_number VARCHAR(32) NOT NULL
  )
"""

ORDERS_TABLE_SCHEMA = """
  CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    order_date DATE NOT NULL
  )
"""

ORDER_ITEMS_TABLE_SCHEMA = """
  CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_sku VARCHAR(64) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0)
  )
"""


def setup_normalized_tables(conn):
    """Drop and recreate 1NF-compliant tables (FK-safe drop order)."""
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS order_items CASCADE")
            cur.execute("DROP TABLE IF EXISTS orders CASCADE")
            cur.execute("DROP TABLE IF EXISTS customer_phone_numbers CASCADE")
            cur.execute("DROP TABLE IF EXISTS customers CASCADE")
            cur.execute(CUSTOMERS_TABLE_SCHEMA)
            cur.execute(CUSTOMER_PHONE_NUMBERS_TABLE_SCHEMA)
            cur.execute(ORDERS_TABLE_SCHEMA)
            cur.execute(ORDER_ITEMS_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating normalized tables:", err)
        raise


def create_indexes(conn):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE INDEX idx_customer_phone_numbers_customer_id "
                "ON customer_phone_numbers (customer_id)"
            )
            cur.execute(
                "CREATE INDEX idx_orders_customer_id ON orders (customer_id)"
            )
            cur.execute(
                "CREATE INDEX idx_order_items_order_id ON order_items (order_id)"
            )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating indexes:", err)
        raise


def normalize_orders(conn):
    """Transform orders_unnormalized into 1NF tables.

    Splits delimited phone numbers and line items into atomic rows.
    Deduplicates customers by name (same name => same customer_id).
    """
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, customer_name, customer_phone_numbers, order_date, line_items
                FROM orders_unnormalized
                ORDER BY id
                """
            )
            rows = cur.fetchall()

            customer_ids = {}

            for _id, customer_name, phones_raw, order_date, line_items_raw in rows:
                if customer_name not in customer_ids:
                    cur.execute(
                        "INSERT INTO customers (name) VALUES (%s) RETURNING id",
                        (customer_name,),
                    )
                    customer_id = cur.fetchone()[0]
                    customer_ids[customer_name] = customer_id

                    for phone in phones_raw.split(","):
                        phone = phone.strip()
                        if phone:
                            cur.execute(
                                """
                                INSERT INTO customer_phone_numbers
                                  (customer_id, phone_number)
                                VALUES (%s, %s)
                                """,
                                (customer_id, phone),
                            )
                else:
                    customer_id = customer_ids[customer_name]

                cur.execute(
                    """
                    INSERT INTO orders (customer_id, order_date)
                    VALUES (%s, %s)
                    RETURNING id
                    """,
                    (customer_id, order_date),
                )
                order_id = cur.fetchone()[0]

                for item in line_items_raw.split(","):
                    item = item.strip()
                    if not item:
                        continue
                    parts = item.split(":")
                    if len(parts) != 3:
                        raise ValueError(f"Invalid line item format: {item!r}")
                    sku, quantity_str, price_str = parts
                    cur.execute(
                        """
                        INSERT INTO order_items
                          (order_id, product_sku, quantity, unit_price_cents)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (order_id, sku, int(quantity_str), int(price_str)),
                    )

        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error normalizing orders:", err)
        raise


def count_customers(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*)::int AS count FROM customers")
        return cur.fetchone()[0]


def count_customer_phone_numbers(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*)::int AS count FROM customer_phone_numbers")
        return cur.fetchone()[0]


def count_orders(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*)::int AS count FROM orders")
        return cur.fetchone()[0]


def count_order_items(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*)::int AS count FROM order_items")
        return cur.fetchone()[0]
