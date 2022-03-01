import json
from typing import Type

from linebot.models import Message

from src.app.postback_handler_base import PostbackHandlerBase
from src.shared.line.postback_action_models import PostbackDataException


class PostbackDispatcherError(Exception):
    pass


class PostbackDispatcher:
    _handler_registry: dict[str, Type[PostbackHandlerBase]]

    def __init__(self):
        self._handler_registry = {}

    def add(self, action: str):
        """
        Register a postback handler.
        Args:
            action: unique action code
        """

        def deco(cls: Type[PostbackHandlerBase]):
            if action in self._handler_registry:
                raise KeyError(
                    f"Postback handler for action '{action}' has been registered."
                )

            self._handler_registry[action] = cls
            return cls

        return deco

    def run_task(self, data: str, source_user_id: str) -> Message:
        action = self._extract_action(data)
        try:
            handler = self._handler_registry[action](data, source_user_id)
            response = handler.execute()
            return response
        except KeyError as e:
            raise PostbackDispatcherError(
                f"No Postback handler registered for the {action} action."
            ) from e
        except PostbackDataException as e:
            raise PostbackDispatcherError(
                "Postback data is not compatible with the registered handler."
            ) from e

    def _extract_action(self, data: str) -> str:
        try:
            return json.loads(data)["action"]
        except json.JSONDecodeError as e:
            raise PostbackDispatcherError(
                "The postback data is not in json format."
            ) from e
        except (KeyError, IndexError) as e:
            raise PostbackDispatcherError(
                "Postback data is not in the right format: no action field."
            ) from e
