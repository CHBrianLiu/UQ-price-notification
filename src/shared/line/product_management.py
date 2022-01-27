from linebot import models

from src.shared.uq.uq_product import UqProduct
from src.shared.line.postback_action_models import ProductRemovalPostbackDataModel


class UqProductManagementTemplateMessageCreator:
    """
    Class for creating the carousel template message for user product management.
    """

    _uq_products: list[UqProduct]

    def __init__(self, products: list[UqProduct]):
        # Decided not to use DI here because we heavily rely on data models.
        self._uq_products = products

    def generate_products_carousel_template_message(self):
        carousel_template_columns = [
            self._generate_product_carousel_column(product)
            for product in self._uq_products
        ]
        template = models.CarouselTemplate(columns=carousel_template_columns)
        return models.TemplateSendMessage(template=template)

    def _generate_product_carousel_column(self, product: UqProduct):
        card_title = product.name
        card_text = f"NT ${product.special_offer}"
        go_website_button = self._generate_product_go_website_action(product)
        removal_button = self._generate_product_removal_action(product)
        return models.CarouselColumn(
            title=card_title,
            text=card_text,
            actions=[go_website_button, removal_button],
        )

    def _generate_product_removal_action(self, product: UqProduct):
        action_button_label = "取消追蹤"
        action_button_click_message = f"取消追蹤 {product.name}"
        postback_data = ProductRemovalPostbackDataModel(
            product_code=product.product_code
        ).json()
        return models.PostbackAction(
            display_text=action_button_click_message,
            label=action_button_label,
            data=postback_data,
        )

    def _generate_product_go_website_action(self, product: UqProduct):
        action_button_label = "前往官網"
        action_button_url = product.website_url
        return models.URIAction(label=action_button_label, uri=action_button_url)
