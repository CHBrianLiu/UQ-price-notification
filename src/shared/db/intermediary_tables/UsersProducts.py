import sqlalchemy

from src.shared import db

users_products = sqlalchemy.Table(
    "users_products",
    db.Base.metadata,
    sqlalchemy.Column("user_id", sqlalchemy.String(100), sqlalchemy.ForeignKey("users.id"), primary_key=True),
    sqlalchemy.Column("product_code", sqlalchemy.String(14), sqlalchemy.ForeignKey("products.product_code"),
                      primary_key=True),
    sqlalchemy.Column("created", sqlalchemy.DateTime, nullable=False),
)
