from flask import Flask

from app.config import Config
from app.extensions import db
from app.routes import bp as api_bp
from app.seed import seed_command


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    app.register_blueprint(api_bp)
    app.cli.add_command(seed_command)

    with app.app_context():
        # Import models so metadata is registered before create_all.
        from app import models  # noqa: F401

        db.create_all()

    return app
