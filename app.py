import random
import configparser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")
# Channel Access Token
#line_bot_api = LineBotApi('eiIQIeDuC6GyB/gn1gBHrri96ZdVS7fwTxqaw0eu7NlCtqj7fxxjNjj27wj3LKS0MEoXDKcqMlqlXRJPRu+6KUroP+F5ZUtXEqmsHiZbTHL9QqusZOF8s5Sot61+rj261DO0Ujmi2RJTfGLMFvxIbwdB04t89/1O/w1cDnyilFU=')
line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
# Channel Secret
#handler = WebhookHandler('3f852273ba31afd703e4116a0a0a37c7')
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = ImageSendMessage(
        original_content_url='https://i.imgur.com/3Kiewj2.jpg',
        preview_image_url='https://i.imgur.com/3Kiewj2.jpg'
    )
    line_bot_api.reply_message(event.reply_token, message)
#def handle_message(event):
    #line_bot_api.reply_message(
        #event.reply_token,
        #TextSendMessage(text=event.message.text+'嗎?'))


if __name__ == "__main__":
    app.run()