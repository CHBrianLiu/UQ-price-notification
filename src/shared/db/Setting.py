import sqlalchemy

from src.shared import db


class Setting(db.Base):
    __tablename__ = "settings"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(), unique=True, nullable=False)
    value = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    last_updated = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
