import logging
from abc import ABCMeta, abstractclassmethod, abstractmethod

from app.config import app_config
from app.line.data_models import UserSource
from app.line.messages import (
    ConfirmTemplateMessage,
    MessageAction,
    TemplateMessage,
    TextMessage,
)
from app.line.postback_data import (
    PostbackDataAdding,
    PostbackDataBase,
    PostbackDataDeleting,
)
from app.line.reply import reply
from app.line.reply_messages import ResponseMessageType, add_messages, delete_messages
from app.models.data_store import data_access
from app.models.Product import Product
from app.models.standard_model import DatabaseOperationError
from app.models.User import User


class PostbackEventHandlerActionBase(metaclass=ABCMeta):
    @abstractclassmethod
    def create(cls):
        pass

    @abstractmethod
    def manipulate(self):
        pass

    @abstractmethod
    async def reply_operation_result(self):
        pass


class PostbackEventHandlerAdding(PostbackEventHandlerActionBase):

    product_id: str
    reply_token: str
    user_id: str
    response: ResponseMessageType

    @classmethod
    def create(cls, raw_data: str, reply_token: str, source: UserSource):
        data = PostbackDataAdding.parse_raw(raw_data)
        return cls(data.product_id, data.product_name, reply_token, source.userId)

    def __init__(
        self, product_id: str, product_name: str, reply_token: str, user_id: str
    ) -> None:
        self.product_id = product_id
        self.product_name = product_name
        self.reply_token = reply_token
        self.user_id = user_id

    def manipulate(self):
        user = self.__get_user_data()
        if self.__is_product_already_in_user_tracking_list(user):
            self.response = ("in_list", {"title": self.product_name})
            return
        if self.__does_reach_tracking_maximum(user):
            self.response = (
                "reach_limit",
                self.__create_confirm_template_for_reaching_limit(),
            )
            return
        self.__add_item_to_list(user)

        if not data_access.is_product_tracked_by_any_user(self.product_id):
            data_access.update_product(Product(product_id=self.product_id))
        data_access.update_user(user)
        self.response = ("tracking", {"title": self.product_name})

    def __get_user_data(self) -> User:
        return (
            data_access.get_user_info(self.user_id)
            if data_access.has_user(self.user_id)
            else User(user_id=self.user_id, count_tracking=0, product_tracking=[])
        )

    def __is_product_already_in_user_tracking_list(self, user: User):
        return self.product_id in user.product_tracking

    def __does_reach_tracking_maximum(self, user: User) -> bool:
        return user.count_tracking >= app_config.TRACKING_ITEM_MAXIMUM

    def __create_confirm_template_for_reaching_limit(self):
        manage_list_action = MessageAction(text="list", label="我的追蹤清單")
        cancel_action = MessageAction(text="cancel", label="我知道了！")
        confirm_template = ConfirmTemplateMessage(
            text="你的追蹤清單已滿！\n來整理一下你的清單吧！", actions=[manage_list_action, cancel_action]
        )
        return TemplateMessage(
            altText="You've reached the limit of number of tracking items.",
            template=confirm_template,
        ).dict(exclude_none=True)

    def __add_item_to_list(self, user: User):
        user.product_tracking.add(self.product_id)
        user.count_tracking += 1

    async def reply_operation_result(self):
        if not hasattr(self, "response") or self.response is None:
            logging.error("manipulate method should be ran first.")
            raise RuntimeError("Reply method ran before manipulate")
        if self.response[0] in add_messages.messages.keys():
            message = TextMessage(
                text=add_messages.messages[self.response[0]].format(
                    **(self.response[1])
                )
            ).dict(exclude_none=True)
        else:
            message = self.response[1]
        await reply(self.reply_token, [message])


class PostbackEventHandlerDeleting(PostbackEventHandlerActionBase):
    @classmethod
    def create(cls, raw_data: str, reply_token: str, source: UserSource):
        data = PostbackDataDeleting.parse_raw(raw_data)
        return cls(data.product_id, reply_token, source.userId)

    def __init__(
        self, product_id: str, reply_token: str, user_id: str
    ) -> None:
        self.product_id = product_id
        self.reply_token = reply_token
        self.user_id = user_id

    def manipulate(self):
        if not data_access.has_user(self.user_id):
            logging.warning("No user data existing: %s", self.user_id)
            self.response = ("no_user", {})
            return
        user_data = data_access.get_user_info(self.user_id)
        if self.product_id not in user_data.product_tracking:
            logging.warning("User tried to delete untracked item.")
            self.response = ("not_tracking", {})
            return
        self.response = self.__delete_tracking_product(user_data)

    def __delete_tracking_product(self, user: User):
        try:
            user.product_tracking.remove(self.product_id)
            user.count_tracking = len(user.product_tracking)
            data_access.update_user(user)
            return ("deleted", {})
        except DatabaseOperationError:
            logging.exception("Delete item error.")
        return ("internal_error", {})

    async def reply_operation_result(self):
        if self.response is None:
            logging.error("manipulate method should be ran first.")
            raise RuntimeError("Reply method ran before manipulate")
        message = delete_messages.messages[self.response[0]].format(
            **(self.response[1])
        )
        await reply(self.reply_token, [{"type": "text", "text": message}])


class PostbackHandlerFactory:
    @staticmethod
    def create(
        raw_data: str, reply_token: str, source: UserSource
    ) -> PostbackEventHandlerActionBase:
        data = PostbackDataBase.parse_raw(raw_data)
        if data.action == "add":
            return PostbackEventHandlerAdding.create(raw_data, reply_token, source)
        if data.action == "delete":
            return PostbackEventHandlerDeleting.create(raw_data, reply_token, source)
        raise RuntimeError(f"Not supported operation: {data.action}")
