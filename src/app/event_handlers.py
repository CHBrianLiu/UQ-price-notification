import linebot
from linebot.models import MessageEvent, TextMessage, PostbackEvent

from src import config
from src.app.text_handlers import text_message_dispatcher
from src.app.postback_handlers import postback_dispatcher

line_api = linebot.LineBotApi(config.LINE_CHANNEL_TOKEN, config.LINE_API_ENDPOINT)
webhook_handler = linebot.WebhookHandler(config.LINE_CHANNEL_SECRET)


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message_event(event: MessageEvent):
    # Currently, only normal users can interact with our bot.
    if event.source.type != "user":
        return

    reply_token = event.reply_token
    message = event.message.text
    user_id = event.source.user_id

    reply_message = text_message_dispatcher.run_task(message, user_id)

    line_api.reply_message(reply_token, reply_message)


@webhook_handler.add(PostbackEvent)
def handle_postback_event(event: PostbackEvent):
    # Currently, only normal users can interact with our bot.
    if event.source.type != "user":
        return
    response = postback_dispatcher.run_task(event.postback.data, event.source.user_id)
    line_api.reply_message(event.reply_token, response)
