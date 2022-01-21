import sqlalchemy
from sqlalchemy import orm

from src.shared import db
from src.shared.db.intermediary_tables import UsersProducts


class User(db.Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.String(100), primary_key=True)
    role_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id"), nullable=False
    )
    created = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    role = orm.relationship("Role")
    products = orm.relationship(
        "Product", secondary=UsersProducts.users_products, backref="users"
    )
