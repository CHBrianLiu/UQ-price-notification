from pydantic import BaseModel


class Product(BaseModel):
    product_id: str
