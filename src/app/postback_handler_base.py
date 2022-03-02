import abc

from linebot.models import Message
from pydantic import ValidationError

from src.shared.line.postback_action_models import (
    PostbackDataModelBase,
    PostbackDataException,
)


class PostbackHandlerBase(abc.ABC):
    _raw_data: str
    _source_user_id: str

    # OVERRIDE
    _DATA_MODEL = PostbackDataModelBase

    _data: _DATA_MODEL

    def __init__(self, raw_data: str, source_user_id: str):
        self._raw_data = raw_data
        self._source_user_id = source_user_id
        self._parse_data()

    def _parse_data(self):
        try:
            self._data = self._DATA_MODEL.parse_raw(self._raw_data)
        except ValidationError as e:
            raise PostbackDataException from e

    @abc.abstractmethod
    def execute(self) -> Message:
        pass
