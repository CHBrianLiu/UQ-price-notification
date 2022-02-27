import abc

from linebot import models

from src.shared.uq.uq_product import UqProduct
from src.shared.line.carousel_column_creators import (
    UqProductManagementTemplateColumnCreator,
)
from src.shared.line.postback_action_models import ProductAddingConfirmationDataModel


class LineMessageCreator(abc.ABC):
    @abc.abstractmethod
    def generate(self) -> models.Message:
        pass


class HelpMessageCreator(LineMessageCreator):
    def generate(self) -> models.TextMessage:
        return models.TextMessage(text="請傳送商品網址")


class PriceDownNotificationMessageCreator(LineMessageCreator):
    def generate(self) -> models.TextMessage:
        return models.TextMessage(text="你好，你追蹤的商品正在特價中！把握機會購買吧！")


class ProductUrlErrorMessageCreator(LineMessageCreator):
    def generate(self) -> models.TextMessage:
        return models.TextMessage(text="你所輸入的商品網址有誤，請重新輸入！")


class UqProductManagementTemplateFactory:
    def get_uq_product_management_template_column_creator(self, *args, **kwargs):
        return UqProductManagementTemplateColumnCreator(*args, **kwargs)


class UqProductManagementTemplateMessageCreator(LineMessageCreator):
    """
    Class for creating the carousel template message for user product management.
    """

    _uq_products: list[UqProduct]

    def __init__(
        self,
        products: list[UqProduct],
        factory: UqProductManagementTemplateFactory = None,
    ):
        # Decided not to use DI here because we heavily rely on data models.
        self._uq_products = products
        self._factory = (
            factory if factory is not None else UqProductManagementTemplateFactory()
        )

    def generate(self) -> models.TemplateSendMessage:
        carousel_template_columns = []
        for product in self._uq_products:
            column_creator = (
                self._factory.get_uq_product_management_template_column_creator(product)
            )
            column = column_creator.generate_product_carousel_column()
            carousel_template_columns.append(column)
        template = models.CarouselTemplate(columns=carousel_template_columns)
        return models.TemplateSendMessage(template=template)


class UqProductSubscriptionConfirmationMessageCreator(LineMessageCreator):
    _product: UqProduct

    def __init__(self, product: UqProduct):
        self._product = product

    def generate(self) -> models.TemplateSendMessage:
        template = self._generate_button_template()
        return models.TemplateSendMessage(template=template)

    def _generate_button_template(self):
        template_title = self._product.name
        template_content = f"NT ${self._product.special_offer}\n你要追蹤此商品嗎？"
        yes_action = self._generate_yes_action()
        no_action = self._generate_no_action()
        return models.ButtonsTemplate(
            title=template_title, text=template_content, actions=[yes_action, no_action]
        )

    def _generate_yes_action(self):
        button_label = "Yes"
        button_text = "Yes"
        button_data = ProductAddingConfirmationDataModel(
            product_code=self._product.product_code
        ).json()
        return models.PostbackAction(
            label=button_label, text=button_text, data=button_data
        )

    def _generate_no_action(self):
        button_label = "No"
        button_text = "No"
        return models.MessageAction(label=button_label, text=button_text)
