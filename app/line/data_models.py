from typing import Dict, List, Union
from typing_extensions import TypedDict

from pydantic import BaseModel


class SourceBase(TypedDict):
    type: str


class UserSource(SourceBase):
    userId: str


class GroupSource(UserSource):
    groupId: str


class RoomSource(UserSource):
    roomId: str


# Can't use TypedDict because it doesn't take extra keys. Make this as reference.
class WebhookEvent(TypedDict):
    type: str
    mode: str
    timestamp: int
    source: Union[UserSource, GroupSource, RoomSource]


class LineRequest(BaseModel):
    destination: str
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
