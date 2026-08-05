import json
import os
from datetime import date, datetime
from decimal import Decimal

import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DATABASE_HOST", "localhost"),
        port=int(os.environ.get("DATABASE_PORT", "5432")),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
        dbname=os.environ.get("COMPOSE_PROJECT_NAME"),
    )


def _json_default(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return int(obj) if obj == obj.to_integral_value() else float(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def query(sql, params=None):
    """Run SQL and pretty-print result rows (for notebooks / exploration)."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            if cur.description is None:
                conn.commit()
                print(f"OK (rowcount={cur.rowcount})")
                return None
            rows = cur.fetchall()
            print(json.dumps(rows, indent=2, default=_json_default))
            return rows
