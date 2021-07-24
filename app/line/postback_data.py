from pydantic import BaseModel, Field


class PostbackDataBase(BaseModel):
    action: str


class PostbackDataAdding(PostbackDataBase):
    action = Field("add", const=True)
    product_id: str
    product_name: str


class PostbackDataDeleting(PostbackDataBase):
    action = Field("delete", const=True)
    product_id: str
