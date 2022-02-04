from pydantic import BaseModel


class ProductRemovalPostbackDataModel(BaseModel):
    action = "remove"
    product_code: str


class ProductAddingConfirmationDataModel(BaseModel):
    action = "add"
    product_code: str
