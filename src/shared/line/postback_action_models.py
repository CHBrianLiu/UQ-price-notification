from pydantic import BaseModel


class ProductRemovalPostbackDataModel(BaseModel):
    action = "remove"
    product_code: str
