from linebot import models

from src.shared.uq.uq_product import UqProduct
from src.shared.line.postback_action_models import ProductRemovalPostbackDataModel


class UqProductManagementTemplateColumnCreator:
    _product: UqProduct

    def __init__(self, product: UqProduct):
        self._product = product

    def generate_product_carousel_column(self):
        card_title = self._product.name
        card_text = self._compose_card_content()
        go_website_button = self._generate_product_go_website_action()
        removal_button = self._generate_product_removal_action()
        return models.CarouselColumn(
            title=card_title,
            text=card_text,
            actions=[go_website_button, removal_button],
        )

    def _generate_product_removal_action(self):
        action_button_label = "取消追蹤"
        action_button_click_message = f"取消追蹤 {self._product.name}"
        postback_data = ProductRemovalPostbackDataModel(
            product_code=self._product.product_code
        ).json()
        return models.PostbackAction(
            display_text=action_button_click_message,
            label=action_button_label,
            data=postback_data,
        )

    def _generate_product_go_website_action(self):
        action_button_label = "前往官網"
        action_button_url = self._product.website_url
        return models.URIAction(label=action_button_label, uri=action_button_url)

    def _compose_card_content(self):
        if self._product.is_on_sale:
            return f"原價：NT$ {self._product.original_price}\n特價：NT$ {self._product.special_offer}"
        return f"NT$ {self._product.original_price}"
