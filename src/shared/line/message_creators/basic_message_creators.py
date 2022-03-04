from linebot import models

from src.shared.line.message_creators.base_creators import LineMessageCreator


class HelpMessageCreator(LineMessageCreator):
    def generate(self) -> models.TextMessage:
        return models.TextMessage(text="請傳送商品網址")


class PriceDownNotificationMessageCreator(LineMessageCreator):
    def generate(self) -> models.TextMessage:
        return models.TextMessage(text="你好，你追蹤的商品正在特價中！把握機會購買吧！")


class ProductUrlErrorMessageCreator(LineMessageCreator):
    def generate(self) -> models.TextMessage:
        return models.TextMessage(text="你所輸入的商品網址有誤，請重新輸入！")


class ProductSuccessfullyAddedMessageCreator(LineMessageCreator):
    product_name: str

    def __init__(self, product_name: str):
        self.product_name = product_name

    def generate(self) -> models.TextMessage:
        return models.TextMessage(text=f"已成功將{self.product_name}加入追蹤清單！")


class ProductAlreadyInListMessageCreator(LineMessageCreator):
    product_name: str

    def __init__(self, product_name: str):
        self.product_name = product_name

    def generate(self) -> models.TextMessage:
        return models.TextMessage(text=f"{self.product_name}已經在你的追蹤清單了喔！")


class ProductNotInListYetMessageCreator(LineMessageCreator):
    def generate(self) -> models.TextMessage:
        return models.TextMessage(text="你還沒追蹤此商品喔！")


class ProductSuccessfullyRemovedMessageCreator(LineMessageCreator):
    product_name: str

    def __init__(self, product_name: str):
        self.product_name = product_name

    def generate(self) -> models.TextMessage:
        return models.TextMessage(text=f"已成功將{self.product_name}從清單移除！")


class NoSubscribedProductMessageCreator(LineMessageCreator):
    def generate(self) -> models.Message:
        return models.TextMessage(text="你沒有追蹤中的商品喔！")
