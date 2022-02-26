from datetime import datetime

import peewee

from src.shared.db import connection


class BaseModel(peewee.Model):
    class Meta:
        database = connection


class Product(BaseModel):
    product_code = peewee.CharField(primary_key=True)
    name = peewee.CharField()
    current_price = peewee.IntegerField()
    original_price = peewee.IntegerField()
    short_description = peewee.TextField()
    last_updated = peewee.DateTimeField(default=datetime.now)


class Setting(BaseModel):
    id = peewee.AutoField()
    name = peewee.CharField(unique=True, index=True)
    value = peewee.CharField()
    last_updated = peewee.DateTimeField(default=datetime.now)


class User(BaseModel):
    id = peewee.CharField(primary_key=True)
    role_id = peewee.IntegerField(null=False)
    created = peewee.DateTimeField(default=datetime.now)


class UserProduct(BaseModel):
    user = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)
