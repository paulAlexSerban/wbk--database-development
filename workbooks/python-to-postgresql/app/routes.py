from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Customer, Order, Product

bp = Blueprint("api", __name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/customers")
def list_customers():
    customers = Customer.query.order_by(Customer.id).all()
    return jsonify([c.to_dict() for c in customers])


@bp.post("/customers")
def create_customer():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    if not email:
        return jsonify({"error": "email is required"}), 400

    if Customer.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 409

    customer = Customer(email=email)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201


@bp.get("/products")
def list_products():
    query = Product.query
    color = request.args.get("color")
    if color:
        query = query.filter(Product.attributes["color"].astext == color)

    products = query.order_by(Product.id).all()
    return jsonify([p.to_dict() for p in products])


@bp.post("/products")
def create_product():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    price_cents = data.get("price_cents")
    attributes = data.get("attributes") or {}

    if not name:
        return jsonify({"error": "name is required"}), 400
    if price_cents is None or not isinstance(price_cents, int) or price_cents < 0:
        return jsonify({"error": "price_cents must be a non-negative integer"}), 400
    if not isinstance(attributes, dict):
        return jsonify({"error": "attributes must be an object"}), 400

    product = Product(name=name, price_cents=price_cents, attributes=attributes)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


@bp.get("/orders")
def list_orders():
    orders = Order.query.order_by(Order.id).all()
    return jsonify([o.to_dict() for o in orders])


@bp.post("/orders")
def create_order():
    data = request.get_json(silent=True) or {}
    customer_id = data.get("customer_id")
    items = data.get("items") or []
    status = (data.get("status") or "pending").strip()

    if not customer_id:
        return jsonify({"error": "customer_id is required"}), 400
    if db.session.get(Customer, customer_id) is None:
        return jsonify({"error": "customer not found"}), 404
    if not isinstance(items, list) or not items:
        return jsonify({"error": "items must be a non-empty array"}), 400

    for item in items:
        if not isinstance(item, dict):
            return jsonify({"error": "each item must be an object"}), 400
        if "product_id" not in item or "quantity" not in item or "unit_price_cents" not in item:
            return jsonify(
                {"error": "each item needs product_id, quantity, unit_price_cents"}
            ), 400

    order = Order(customer_id=customer_id, status=status, items=items)
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_dict()), 201
