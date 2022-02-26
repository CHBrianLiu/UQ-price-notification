import peewee

from src import config

connection = peewee.PostgresqlDatabase(
    config.DATABASE_NAME,
    user=config.DATABASE_USER,
    password=config.DATABASE_PASSWORD,
    host=config.DATABASE_HOST,
)
