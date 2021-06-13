from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel
from pydantic.fields import Field


class MessageBase(BaseModel):
    type: str
    text: str


class EmojiInTextMessage(BaseModel):
    index: int
    productId: str
    emojiId: str


class TextMessage(MessageBase):
    type: str = Field("text", const=True)
    emojis: Optional[List[EmojiInTextMessage]]


class MessageAction(BaseModel):
    type: str = Field("message", const=True)
    label: Optional[str] = Field(max_length=20)
    text: str = Field(max_length=300)


class UriAction(BaseModel):
    type: str = Field("uri", const=True)
    label: Optional[str] = Field(max_length=20)
    uri: str = Field(max_length=1000)


class CarouselTemplateColumn(BaseModel):
    text: str = Field(max_length=120)
    actions: List[Union[MessageAction, UriAction]]
    thumbnailImageUrl: Optional[str]
    imageBackgroundColor: Optional[str]
    title: str = Field(max_length=40)
    defaultAction: Optional[Union[MessageAction, UriAction]]


class CarouselTemplateImageRatio(str, Enum):
    rectangle = "rectangle"
    square = "square"


class CarouselTemplateImageSize(str, Enum):
    cover = "cover"
    contain = "contain"


class ButtonTemplateMessage(BaseModel):
    type: str = Field("buttons", const=True)
    title: Optional[str] = Field(max_length=40)
    text: str = Field(max_length=160)
    actions: List[Union[MessageAction, UriAction]] = Field(max_items=4)
    defaultAction: Optional[Union[MessageAction, UriAction]]
    thumbnailImageUrl: Optional[str] = Field(max_length=1000)
    imageAspectRatio: CarouselTemplateImageRatio = CarouselTemplateImageRatio.rectangle
    imageSize: CarouselTemplateImageSize = CarouselTemplateImageSize.cover
    imageBackgroundColor: Optional[str]


class ConfirmTemplateMessage(BaseModel):
    type: str = Field("confirm", const=True)
    text: str = Field(max_length=240)
    actions: List[Union[MessageAction, UriAction]] = Field(min_items=2, max_items=2)


class CarouselTemplateMessage(BaseModel):
    type: str = Field("carousel", const=True)
    columns: List[CarouselTemplateColumn] = Field(max_items=10)
    imageAspectRatio: CarouselTemplateImageRatio = CarouselTemplateImageRatio.rectangle
    imageSize: CarouselTemplateImageSize = CarouselTemplateImageSize.cover


class TemplateMessage(BaseModel):
    type: str = Field("template", const=False)
    altText: str = Field(max_length=400)
    template: Union[
        CarouselTemplateMessage, ButtonTemplateMessage, ConfirmTemplateMessage
    ]
