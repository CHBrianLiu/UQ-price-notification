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
