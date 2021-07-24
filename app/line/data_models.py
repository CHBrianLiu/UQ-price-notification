from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel
from pydantic.fields import Field


class SourceBase(BaseModel):
    type: str


class UserSource(SourceBase):
    userId: str


class GroupSource(UserSource):
    groupId: str


class RoomSource(UserSource):
    roomId: str


class EventMode(str, Enum):
    active = "active"
    standby = "standby"


# Can't use TypedDict because it doesn't take extra keys. Make this as reference.
class WebhookEventBase(BaseModel):
    type: str
    mode: EventMode
    timestamp: int
    source: Union[UserSource, GroupSource, RoomSource]


class PostbackEventPostback(BaseModel):
    data: str
    params: Optional[Dict[str, str]]


class PostbackEvent(WebhookEventBase):
    replyToken: str
    type: str = Field("postback", const=True)
    postback: PostbackEventPostback


class LineRequest(BaseModel):
    destination: Optional[str]
    events: List[
        Dict[str, Union[str, dict, Union[UserSource, GroupSource, RoomSource]]]
    ]


EventType = Dict[
    str,
    Union[
        str,
        dict,
        Union[UserSource, GroupSource, RoomSource],
    ],
]
