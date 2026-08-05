import string

from faker import Faker

fake = Faker()
_ALPHANUMERIC = string.ascii_letters + string.digits

CUSTOMERS_TABLE_SCHEMA = """
  CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
  )
"""


def generate_customers(count):
    return [{"email": fake.email()} for _ in range(count)]


CUSTOMERS = generate_customers(100)


def setup_customers_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS customers CASCADE")
            cur.execute(CUSTOMERS_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating customers table:", err)
        raise


def insert_customers(conn, customers):
    try:
        with conn.cursor() as cur:
            for customer in customers:
                cur.execute(
                    "INSERT INTO customers (email) VALUES (%s)",
                    (customer["email"],),
                )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error inserting customers:", err)
        raise


def count_customers(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*)::int AS count FROM customers")
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting customers:", err)
        raise


ORDERS_TABLE_SCHEMA = """
  CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
  )
"""


def generate_orders(count):
    return [
        {
            "customer_id": fake.random_int(min=1, max=100),
            "status": fake.random_element(elements=["pending", "shipped", "delivered"]),
        }
        for _ in range(count)
    ]


ORDERS = generate_orders(100)


def setup_orders_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS orders CASCADE")
            cur.execute(ORDERS_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating orders table:", err)
        raise


def insert_orders(conn, orders):
    try:
        with conn.cursor() as cur:
            for order in orders:
                cur.execute(
                    "INSERT INTO orders (customer_id, status) VALUES (%s, %s)",
                    (order["customer_id"], order["status"]),
                )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error inserting orders:", err)
        raise


def count_orders(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*)::int AS count FROM orders")
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting orders:", err)
        raise


ORDER_ITEMS_TABLE_SCHEMA = """
  CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_sku VARCHAR(64) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_cents INTEGER NOT NULL CHECK (unit_price_cents >= 0)
  )
"""


def generate_order_items(count):
    return [
        {
            "order_id": fake.random_int(min=1, max=100),
            "product_sku": "".join(
                fake.random_choices(elements=_ALPHANUMERIC, length=64)
            ),
            "quantity": fake.random_int(min=1, max=100),
            "unit_price_cents": fake.random_int(min=0, max=10000),
        }
        for _ in range(count)
    ]


ORDER_ITEMS = generate_order_items(10000)


def setup_order_items_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS order_items CASCADE")
            cur.execute(ORDER_ITEMS_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating order items table:", err)
        raise


def insert_order_items(conn, order_items):
    try:
        with conn.cursor() as cur:
            for order_item in order_items:
                cur.execute(
                    "INSERT INTO order_items (order_id, product_sku, quantity, unit_price_cents) VALUES (%s, %s, %s, %s)",
                    (
                        order_item["order_id"],
                        order_item["product_sku"],
                        order_item["quantity"],
                        order_item["unit_price_cents"],
                    ),
                )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error inserting order items:", err)
        raise


def count_order_items(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*)::int AS count FROM order_items")
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting order items:", err)
        raise


def create_indexes(conn):
    try:
        with conn.cursor() as cur:
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


def join_across_all_tables(conn):
    query = """
    SELECT
      o.id AS order_id,
      c.email,
      o.status,
      SUM(oi.quantity * oi.unit_price_cents) AS total_cents
    FROM orders o
    JOIN customers c ON c.id = o.customer_id
    JOIN order_items oi ON oi.order_id = o.id
    WHERE o.status = 'pending'
    GROUP BY o.id, c.email, o.status
    ORDER BY o.created_at DESC
    LIMIT 50
    """

    try:
        with conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    except Exception as err:
        print("Error joining across all tables:", err)
        raise
