import unittest
from unittest import mock

from src.app.text_handlers.text_dispatcher import (
    TextMessageDispatcher,
    ITextMessageHandler,
    TextMessageDispatcherError,
)


class TestTextMessageDispatcher(unittest.TestCase):
    def test_add_decorator_should_register_handler_class(self):
        dispatcher = TextMessageDispatcher()

        @dispatcher.add
        class Handler(ITextMessageHandler):
            def is_command(message: str):
                pass

            def __init__(self):
                pass

            def execute(self):
                pass

        self.assertIn(Handler.__name__, dispatcher._handler_registry)
        self.assertIs(Handler, dispatcher._handler_registry[Handler.__name__])

    def test_add_decorator_should_raise_exception_when_non_text_message_handler_registered(
        self,
    ):
        dispatcher = TextMessageDispatcher()

        with self.assertRaisesRegex(ValueError, "ITextMessageHandler"):

            @dispatcher.add
            class Handler:
                pass

    def test_add_decorator_should_raise_exception_when_handler_registered_repeatedly(
        self,
    ):
        dispatcher = TextMessageDispatcher()

        @dispatcher.add
        class Handler(ITextMessageHandler):
            def is_command(message: str):
                pass

            def __init__(self):
                pass

            def execute(self):
                pass

        with self.assertRaisesRegex(KeyError, "registered"):

            @dispatcher.add
            class Handler(ITextMessageHandler):
                def is_command(message: str):
                    pass

                def __init__(self):
                    pass

                def execute(self):
                    pass

    def test_add_default_decorator_should_register_handler_as_default_handler(self):
        dispatcher = TextMessageDispatcher()

        @dispatcher.add_default
        class Handler(ITextMessageHandler):
            def is_command(message: str):
                pass

            def __init__(self):
                pass

            def execute(self):
                pass

        self.assertIs(Handler, dispatcher._default_handler)

    def test_add_default_decorator_should_raise_exception_when_non_text_message_handler_registered(
        self,
    ):
        dispatcher = TextMessageDispatcher()

        with self.assertRaisesRegex(ValueError, "ITextMessageHandler"):

            @dispatcher.add_default
            class Handler:
                pass

    def test_add_default_decorator_should_raise_exception_when_handler_registered_repeatedly(
        self,
    ):
        dispatcher = TextMessageDispatcher()

        @dispatcher.add_default
        class Handler1(ITextMessageHandler):
            def is_command(message: str):
                pass

            def __init__(self):
                pass

            def execute(self):
                pass

        with self.assertRaisesRegex(KeyError, "registered"):

            @dispatcher.add_default
            class Handler2(ITextMessageHandler):
                def is_command(message: str):
                    pass

                def __init__(self):
                    pass

                def execute(self):
                    pass

    def test_run_task_should_call_execute_when_one_handler_fit_the_message(self):
        dispatcher = TextMessageDispatcher()

        @dispatcher.add
        class Handler(ITextMessageHandler):
            def __init__(self, message: str, source_user_id: str):
                pass

            @staticmethod
            def is_command(message: str):
                return True

            def execute(self):
                return "message"

        message = dispatcher.run_task("Any message will fit the mock handler", "user")
        self.assertEqual("message", message)

    def test_run_task_should_use_default_handler_if_no_handler_matches(self):
        dispatcher = TextMessageDispatcher()

        @dispatcher.add
        class Handler(ITextMessageHandler):
            def __init__(self, message: str, source_user_id: str):
                pass

            @staticmethod
            def is_command(message: str):
                return False

            def execute(self):
                return "not this one"

        @dispatcher.add_default
        class DefaultHandler(ITextMessageHandler):
            def __init__(self, message: str, source_user_id: str):
                pass

            @staticmethod
            def is_command(message: str):
                pass

            def execute(self):
                return "use default"

        message = dispatcher.run_task("message", "user_id")
        self.assertIs("use default", message)

    def test_run_task_should_raise_exception_if_no_handler(self):
        dispatcher = TextMessageDispatcher()

        @dispatcher.add
        class Handler(ITextMessageHandler):
            def __init__(self, message: str, source_user_id: str):
                pass

            @staticmethod
            def is_command(message: str):
                return False

            def execute(self):
                return "not this one"

        with self.assertRaisesRegex(TextMessageDispatcherError, "No matched handler"):
            dispatcher.run_task("message", "user_id")
