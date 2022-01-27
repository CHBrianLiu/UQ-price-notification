from linebot import models

from src.shared.uq.uq_product import UqProduct
from src.shared.line.postback_action_models import ProductAddingConfirmationDataModel


class UqProductSubscriptionConfirmationMessageCreator:
    _product: UqProduct

    def __init__(self, product: UqProduct):
        self._product = product

    def generate_product_subscription_confirmation_message(self):
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
