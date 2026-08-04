import click
from flask.cli import with_appcontext

from app.extensions import db
from app.models import Customer, Order, Product


@click.command("seed")
@with_appcontext
def seed_command():
    """Seed demo customers, products (JSONB attributes), and orders (JSONB items)."""
    db.session.query(Order).delete()
    db.session.query(Product).delete()
    db.session.query(Customer).delete()
    db.session.commit()

    customers = [
        Customer(email="alice@example.com"),
        Customer(email="bob@example.com"),
        Customer(email="carol@example.com"),
    ]
    db.session.add_all(customers)
    db.session.flush()

    products = [
        Product(
            name="Classic Tee",
            price_cents=1999,
            attributes={"color": "red", "size": "M", "tags": ["sale", "cotton"]},
        ),
        Product(
            name="Denim Jacket",
            price_cents=7999,
            attributes={"color": "blue", "size": "L", "tags": ["outerwear"]},
        ),
        Product(
            name="Running Shoes",
            price_cents=12999,
            attributes={"color": "red", "size": "42", "tags": ["sport", "sale"]},
        ),
        Product(
            name="Wool Scarf",
            price_cents=2499,
            attributes={"color": "green", "size": "one", "tags": ["accessory"]},
        ),
    ]
    db.session.add_all(products)
    db.session.flush()

    orders = [
        Order(
            customer_id=customers[0].id,
            status="pending",
            items=[
                {
                    "product_id": products[0].id,
                    "quantity": 2,
                    "unit_price_cents": products[0].price_cents,
                },
                {
                    "product_id": products[2].id,
                    "quantity": 1,
                    "unit_price_cents": products[2].price_cents,
                },
            ],
        ),
        Order(
            customer_id=customers[1].id,
            status="shipped",
            items=[
                {
                    "product_id": products[1].id,
                    "quantity": 1,
                    "unit_price_cents": products[1].price_cents,
                }
            ],
        ),
    ]
    db.session.add_all(orders)
    db.session.commit()

    click.echo(
        f"Seeded {len(customers)} customers, {len(products)} products, {len(orders)} orders"
    )
