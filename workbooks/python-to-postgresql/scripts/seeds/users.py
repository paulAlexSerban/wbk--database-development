from faker import Faker

fake = Faker()

USERS_TABLE_SCHEMA = """
    CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      username TEXT NOT NULL,
      password TEXT NOT NULL
    )
"""


def generate_users(count):
    return [
        {
            "username": fake.user_name(),
            "password": fake.password(),
        }
        for _ in range(count)
    ]


USERS = generate_users(100)


def setup_users_table(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS users")
            cur.execute(USERS_TABLE_SCHEMA)
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error creating users table:", err)
        raise


def insert_users(conn, users):
    try:
        with conn.cursor() as cur:
            for user in users:
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (user["username"], user["password"]),
                )
        conn.commit()
    except Exception as err:
        conn.rollback()
        print("Error inserting users:", err)
        raise


def count_users(conn):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*)::int AS count FROM users")
            return cur.fetchone()[0]
    except Exception as err:
        print("Error counting users:", err)
        raise
