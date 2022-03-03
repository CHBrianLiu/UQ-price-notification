import abc
from typing import Type

from linebot import models


class ITextMessageHandler(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def is_command(message: str) -> bool:
        pass

    @abc.abstractmethod
    def __init__(self, message: str, source_user_id: str):
        pass

    @abc.abstractmethod
    def execute(self) -> models.Message:
        pass


class TextMessageDispatcherError(Exception):
    pass


class TextMessageDispatcher:
    _handler_registry: dict[str, Type[ITextMessageHandler]]
    _default_handler: Type[ITextMessageHandler] | None

    def __init__(self):
        self._handler_registry = {}
        self._default_handler = None

    def _check_interface_implementation(self, cls):
        if not issubclass(cls, ITextMessageHandler):
            raise ValueError(
                "Only class implement ITextMessageHandler can be registered."
            )

    @property
    def add(self):
        """
        Register a text message handler.

        IMPORTANT: The sequence of handler registration doesn't matter.
        Make sure only one handler fit in any given message.
        """

        def deco(cls: Type[ITextMessageHandler]):
            self._check_interface_implementation(cls)
            if cls.__name__ in self._handler_registry:
                raise KeyError(
                    f"Text message handler {cls.__name__} has been registered before."
                )

            self._handler_registry[cls.__name__] = cls
            return cls

        return deco

    @property
    def add_default(self):
        """
        Register a default text message handler.
        If the text message doesn't match the requirement from any handler,
        default handler will be invoked.
        """

        def deco(cls: Type[ITextMessageHandler]):
            self._check_interface_implementation(cls)
            if self._default_handler is not None:
                raise KeyError(
                    "Default text message handler has been registered before."
                )
            self._default_handler = cls
            return cls

        return deco

    def run_task(self, message: str, source_user_id: str) -> models.Message:
        handler_class = self._select_handler(message)
        if handler_class is None:
            raise TextMessageDispatcherError(
                "No matched handler. (no default handler registered)"
            )
        handler = handler_class(message, source_user_id)
        response = handler.execute()
        return response

    def _select_handler(self, message: str):
        for registered_handler in self._handler_registry.values():
            if registered_handler.is_command(message):
                return registered_handler
        return self._default_handler
