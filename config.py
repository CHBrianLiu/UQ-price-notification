import os

# Use the template to add a config
# NAME = os.environ.get("NAME", "DEFAULT")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "db")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "uq")
DATABASE_USER = os.environ.get("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password")

LINE_CHANNEL_TOKEN = os.environ.get("LINE_CHANNEL_TOKEN", "")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
# We can replace this config to test Line Messaging API locally
LINE_API_ENDPOINT = os.environ.get("LINE_API_ENDPOINT", "http://line-simulator:8080")
