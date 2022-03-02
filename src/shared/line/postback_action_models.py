from pydantic import BaseModel


class PostbackDataException(Exception):
    pass


class PostbackDataModelBase(BaseModel):
    action: str


class ProductRemovalPostbackDataModel(PostbackDataModelBase):
    action = "remove"
    product_code: str


class ProductAddingConfirmationDataModel(PostbackDataModelBase):
    action = "add"
    product_code: str
