import sqlalchemy

from src.shared import db


class Role(db.Base):
    __tablename__ = "roles"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(16), unique=True, nullable=False)
    permission = sqlalchemy.Column(sqlalchemy.JSON)
