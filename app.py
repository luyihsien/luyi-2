import random
import configparser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('JQ/qPlr4T2I7hnOaFX98TH4deF8qB/xcP6sN1Z43VE+1CbopBwuNi/AvDyVL+uvhMEoXDKcqMlqlXRJPRu+6KUroP+F5ZUtXEqmsHiZbTHJfnEcezNRnjqw1VQ53y9DpFn06OW8zowCX/ivqpKvZMAdB04t89/1O/w1cDnyilFU=')
#line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
# Channel Secret
handler = WebhookHandler('3f852273ba31afd703e4116a0a0a37c7')
#handler = WebhookHandler(config['line_bot']['Channel_Secret'])
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


#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
    #message = ImageSendMessage(
        #original_content_url='https://i.imgur.com/3Kiewj2.jpg',
        #preview_image_url='https://i.imgur.com/3Kiewj2.jpg'
    #)
    #line_bot_api.reply_message(event.reply_token, message)
#def handle_message(event):
    #line_bot_api.reply_message(
        #event.reply_token,
        #TextSendMessage(text=event.message.text+'嗎?'))
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    print(msg)
    if msg=="我要學國文":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="今天的每日一字"))
    if msg=="我要學英文":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="今天的英文影片精選"))
    if msg=="我要學數學":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="這是今天的數學題目"))
    if msg=="9487":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="94狂"))

    '''if event.message.text == "擲骰子遊戲":
        buttons_template = TemplateSendMessage(
            alt_text='擲骰子比大小 template',
            template=ButtonsTemplate(
                title='比大小遊戲',
                text='任選數字1-6',
                thumbnail_image_url='https://i.imgur.com/lSSWPnX.jpg',
                actions=[
                    MessageTemplateAction(
                        label='1',
                        text='1'
                    ),
                    MessageTemplateAction(
                        label='2',
                        text='2'
                    ),
                    MessageTemplateAction(
                        label='3',
                        text='3'
                    ),
                    MessageTemplateAction(
                        label='4',
                        text='4'
                    ),
                    MessageTemplateAction(
                        label='5',
                        text='5'
                    ), MessageTemplateAction(
                        label='6',
                        text='6'
                    )
                ]
            )
        )
'''

    else:
        buttons_template = TemplateSendMessage(
        alt_text='目錄 ',
        template=ButtonsTemplate(
            title='選擇服務',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/3Kiewj2.jpg',
            actions=[
                MessageTemplateAction(
                    label='擲骰子遊戲',
                    text='擲骰子遊戲'
                ),
                MessageTemplateAction(
                    label='開始學習',
                    text='開始學習'
                ),
                URITemplateAction(
                    label='我的fb粉專',
                    uri='https://www.facebook.com/shareteacher/'
                ),
                URITemplateAction(
                    label='正方形人 LINE貼圖',
                    uri='https://store.line.me/stickershop/product/3002176/zh-Hant'
                )#,
                #URITemplateAction(
                    #label='聯絡作者',
                    #uri='https://www.facebook.com/TWTRubiks?ref=bookmarks'
                #)
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)
if __name__ == "__main__":
    app.run()