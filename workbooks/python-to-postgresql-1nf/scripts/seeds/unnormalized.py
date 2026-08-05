import string

from faker import Faker

fake = Faker()
_ALPHANUMERIC = string.ascii_letters + string.digits

ORDERS_UNNORMALIZED_TABLE_SCHEMA = """
  CREATE TABLE orders_unnormalized (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone_numbers VARCHAR(255) NOT NULL,
    order_date DATE NOT NULL,
    line_items TEXT NOT NULL
  )
"""


def _random_phone():
    return fake.numerify(text="555-####")


def _random_sku(length=8):
    return "".join(fake.random_choices(elements=_ALPHANUMERIC, length=length))


def generate_unnormalized_orders(count):
    """Generate orders that violate 1NF via delimited multi-valued columns.

    customer_phone_numbers: comma-separated phones, e.g. "555-0101,555-0199"
    line_items: comma-separated sku:qty:price_cents, e.g. "ABC:2:1999,DEF:1:499"
    """
    rows = []
    for _ in range(count):
        phone_count = fake.random_int(min=1, max=3)
        phones = [_random_phone() for _ in range(phone_count)]

        item_count = fake.random_int(min=1, max=4)
        items = []
        for _ in range(item_count):
            sku = _random_sku()
            quantity = fake.random_int(min=1, max=10)
            unit_price_cents = fake.random_int(min=100, max=10000)
            items.append(f"{sku}:{quantity}:{unit_price_cents}")

        rows.append(
            {
                "customer_name": fake.name(),
                "customer_phone_numbers": ",".join(phones),
                "order_date": fake.date_between(start_date="-1y", end_date="today"),
                "line_items": ",".join(items),
            }
        )
    return rows


UNNORMALIZED_ORDERS = generate_unnormalized_orders(50)


def setup_orders_unnormalized_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS orders_unnormalized CASCADE")
            cur.execute(ORDERS_UNNORMALIZED_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating orders_unnormalized table:", err)
        raise


def insert_unnormalized_orders(conn, orders):
    try:
        with conn.cursor() as cur:
            for order in orders:
                cur.execute(
                    """
                    INSERT INTO orders_unnormalized
                      (customer_name, customer_phone_numbers, order_date, line_items)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        order["customer_name"],
                        order["customer_phone_numbers"],
                        order["order_date"],
                        order["line_items"],
                    ),
                )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error inserting unnormalized orders:", err)
        raise


def count_unnormalized_orders(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*)::int AS count FROM orders_unnormalized")
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting unnormalized orders:", err)
        raise
