from sqlalchemy import orm

Base = orm.declarative_base()

from src.shared.db import Product, Role, Setting, User
