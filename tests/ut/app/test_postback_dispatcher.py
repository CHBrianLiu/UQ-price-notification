import unittest
from unittest import mock

from src.app.postback_dispatcher import PostbackDispatcher, PostbackDispatcherError
from src.shared.line.postback_action_models import PostbackDataException


class TestPostbackDispatcher(unittest.TestCase):
    def test_using_add_decorator_to_register_handler(self):
        dispatcher = PostbackDispatcher()

        @dispatcher.add("add")
        class Handler(mock.MagicMock):
            pass

        self.assertIn("add", dispatcher._handler_registry)
        self.assertIs(Handler, dispatcher._handler_registry["add"])

    def test_using_add_decorator_to_add_duplicated_handler_should_raise_key_error(self):
        dispatcher = PostbackDispatcher()

        @dispatcher.add("add")
        class Handler1(mock.MagicMock):
            pass

        with self.assertRaisesRegex(
            KeyError, "Postback handler for action 'add' has been registered."
        ):

            @dispatcher.add("add")
            class Handler2(mock.MagicMock):
                pass

    def test_run_task_should_raise_exception_if_data_is_not_json_format(self):
        dispatcher = PostbackDispatcher()
        with self.assertRaisesRegex(
            PostbackDispatcherError, "The postback data is not in json format."
        ):
            dispatcher.run_task("not json-parsable data", "user_id")

    def test_run_task_should_raise_exception_if_data_has_no_action_field(self):
        dispatcher = PostbackDispatcher()
        with self.assertRaisesRegex(PostbackDispatcherError, "no action field."):
            dispatcher.run_task("{}", "user_id")

    def test_run_task_should_raise_exception_if_no_corresponding_handler_registered(
        self,
    ):
        dispatcher = PostbackDispatcher()
        with self.assertRaisesRegex(
            PostbackDispatcherError,
            "No Postback handler registered for the no_handler action.",
        ):
            dispatcher.run_task('{"action": "no_handler"}', "user_id")

    def test_run_task_should_raise_exception_if_data_parsing_failed(self):
        dispatcher = PostbackDispatcher()

        @dispatcher.add("add")
        class Handler(mock.MagicMock):
            pass

        Handler.__init__ = mock.MagicMock(side_effect=PostbackDataException)

        with self.assertRaisesRegex(
            PostbackDispatcherError,
            "Postback data is not compatible with the registered handler.",
        ):
            dispatcher.run_task('{"action": "add"}', "user_id")

    def test_run_task_should_return_result_of_execute_method_of_registered_handler(
        self,
    ):
        dispatcher = PostbackDispatcher()
        response = "response message object"

        @dispatcher.add("add")
        class Handler(mock.MagicMock):
            def execute(self):
                return response

        actual_response = dispatcher.run_task('{"action": "add"}', "user_id")

        self.assertIs(actual_response, response)
