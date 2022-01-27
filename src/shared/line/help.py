from linebot import models


class HelpMessageCreator:
    def generate_help_message(self):
        return models.TextMessage(text="請傳送商品網址")
