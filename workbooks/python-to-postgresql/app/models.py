from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import JSONB

from app.extensions import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    orders = db.relationship("Order", back_populates="customer", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Product(db.Model):
    __tablename__ = "products"
    __table_args__ = (
        db.Index("ix_products_attributes", "attributes", postgresql_using="gin"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)
    attributes = db.Column(JSONB, nullable=False, default=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price_cents": self.price_cents,
            "attributes": self.attributes or {},
        }


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )
    status = db.Column(db.String(64), nullable=False, default="pending")
    items = db.Column(JSONB, nullable=False, default=list)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    customer = db.relationship("Customer", back_populates="orders")

    def total_cents(self):
        return sum(
            int(item.get("quantity", 0)) * int(item.get("unit_price_cents", 0))
            for item in (self.items or [])
        )

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "status": self.status,
            "items": self.items or [],
            "total_cents": self.total_cents(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
