import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://admin:admin@localhost:5432/python-to-postgresql",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
