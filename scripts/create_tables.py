from src.shared.db.models import BaseModel
from src.shared.db import connection

if __name__ == '__main__':
    connection.create_tables([cls for cls in BaseModel.__subclasses__()])
