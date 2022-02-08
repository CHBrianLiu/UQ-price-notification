from linebot import models


class HelpMessageCreator:
    def generate_help_message(self):
        return models.TextMessage(text="請傳送商品網址")


class PriceDownNotificationMessageCreator:
    def generate_price_down_notification_message(self):
        return models.TextMessage(text="你好，你追蹤的商品正在特價中！把握機會購買吧！")


class ProductUrlErrorMessageCreator:
    def generate_product_url_error_message(self):
        return models.TextMessage(text="你所輸入的商品網址有誤，請重新輸入！")
