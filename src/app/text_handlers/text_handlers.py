from linebot import models
import requests

from src.app.text_handlers.text_dispatcher import (
    ITextMessageHandler,
    TextMessageDispatcher,
)
from src.shared.line.message_creators.basic_message_creators import (
    HelpMessageCreator,
    ProductUrlErrorMessageCreator,
    NoSubscribedProductMessageCreator,
)
from src.shared.line.message_creators.template_message_creators import (
    UqProductSubscriptionConfirmationMessageCreator,
    UqProductManagementTemplateMessageCreator,
)
from src.shared.uq.uq_url_utils import UqProductCodeParser
from src.shared.uq.uq_product import UqRetriever, UqProduct, UqProductException
from src.shared.db.utils import UserDataRetriever
from src.shared.db.models import User, Product

text_message_dispatcher = TextMessageDispatcher()


class TextMessageHandlerBase(ITextMessageHandler):
    _message: str
    _source_user_id: str

    def __init__(self, message: str, source_user_id: str):
        super(TextMessageHandlerBase, self).__init__(message, source_user_id)
        self._message = message
        self._source_user_id = source_user_id


@text_message_dispatcher.add_default
class DefaultTextMessageHandler(TextMessageHandlerBase):
    @staticmethod
    def is_command(message: str) -> bool:
        """
        This method doesn't matter when it's a default message handler.
        """
        return True

    def execute(self) -> models.Message:
        return HelpMessageCreator().generate()


@text_message_dispatcher.add
class ProductUrlTextMessageHandler(TextMessageHandlerBase):
    @staticmethod
    def is_command(message: str) -> bool:
        return UqProductCodeParser(message).get_product_code_from_url() is not None

    def execute(self) -> models.Message:
        product_code = UqProductCodeParser(self._message).get_product_code_from_url()
        try:
            with requests.Session() as session:
                retriever = UqRetriever(product_code, session)
                product = UqProduct(retriever)
                message = UqProductSubscriptionConfirmationMessageCreator(
                    product
                ).generate()

        except UqProductException:
            message = ProductUrlErrorMessageCreator().generate()

        return message


@text_message_dispatcher.add
class ProductListTextMessageHandler(TextMessageHandlerBase):
    @staticmethod
    def is_command(message: str) -> bool:
        return message == "管理個人清單"

    def execute(self) -> models.Message:
        (user, _) = User.get_or_create(id=self._source_user_id, role_id=1)
        products = UserDataRetriever(user).get_subscribed_products()

        if not products:
            return NoSubscribedProductMessageCreator().generate()

        return self._generate_message_from_product_list(products)

    def _generate_message_from_product_list(self, products: dict[str, Product]):
        with requests.Session() as session:
            uq_products = [
                UqProduct(UqRetriever(code, session)) for code in products.keys()
            ]
            return UqProductManagementTemplateMessageCreator(uq_products).generate()
