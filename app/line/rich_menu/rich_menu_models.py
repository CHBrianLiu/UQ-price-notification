from typing import List, Optional, Union

from pydantic import BaseModel, Field

from app.line.messages import MessageAction, UriAction


class RichMenuSize(BaseModel):
    width: int
    height: int


class RichMenuBounds(BaseModel):
    x: int
    y: int
    width: int
    height: int


class RichMenuArea(BaseModel):
    bounds: RichMenuBounds
    action: Union[MessageAction, UriAction]


class RichMenu(BaseModel):
    richMenuId: Optional[str]
    size: RichMenuSize
    selected: bool
    name: str = Field(max_length=300)
    chatBarText: str = Field(max_length=14)
    areas: List[RichMenuArea] = Field(max_items=20)
