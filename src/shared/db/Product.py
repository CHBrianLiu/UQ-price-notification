import sqlalchemy

from src.shared import db


class Product(db.Base):
    __tablename__ = "products"

    product_code = sqlalchemy.Column(sqlalchemy.String(14), primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    current_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    original_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    short_description = sqlalchemy.Column(sqlalchemy.String())
    last_updated = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
