import requests
import random
from bs4 import BeautifulSoup
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

def guess_number():
    num=random.randint(1, 4)
    return (num)


def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content
def movie():
    target_url = 'https://movies.yahoo.com.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('div.movielist_info h1 a')):
        if index == 20:
            return content
        print("data：")
        print(index)
        print(data)
        title = data.text
        link =  data['href']
        content += '{}\n{}\n'.format(title, link)
    return content
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    msg = event.message.text
    print(msg)
    if msg=="國文":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="今天的每日一字"))
    if msg=="英文":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="今天的英文影片精選"))
    if msg=="數學":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="這是今天的數學題目"))
    if msg=="9487":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="94狂"))
    if msg=="最新電影":
        a = movie()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=a))

    if event.message.text == "開始學習":
        buttons_template = TemplateSendMessage(
            alt_text='開始學習',
            template=ButtonsTemplate(
                title='學習日記',
                text='你要學什麼',
                thumbnail_image_url='https://i.imgur.com/1M5VCS1.jpg',
                actions=[
                    MessageTemplateAction(
                        label='國文',
                        text='國文'
                    ),
                    MessageTemplateAction(
                        label='英文',
                        text='英文'
                    ),
                    MessageTemplateAction(
                        label='數學',
                        text='數學'
                    ),
                    MessageTemplateAction(
                        label='輕鬆一下',
                        text='輕鬆一下'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

    if event.message.text == "輕鬆一下":
        buttons_template = TemplateSendMessage(
            alt_text='輕鬆一下',
            template=ButtonsTemplate(
                title='輕鬆一下',
                text='看個電影或新聞吧',
                thumbnail_image_url='https://i.imgur.com/IOYaJS2.jpg',
                actions=[
                    MessageTemplateAction(
                        label='最新電影',
                        text='最新電影'
                    ),
                    MessageTemplateAction(
                        label='科技新聞',
                        text='科技新聞'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "瓶中信遊戲":
        buttons_template = TemplateSendMessage(
            alt_text='開始玩 template',
            template=ButtonsTemplate(
                title='瓶中信遊戲',
                text='選擇瓶子內1-4號信   拆一封信送給你',
                thumbnail_image_url='https://i.imgur.com/HuP4FiS.jpg',
                actions=[
                    MessageTemplateAction(
                        label='1號信',
                        text='1號信'
                    ),
                    MessageTemplateAction(
                        label='2號信',
                        text='2號信'
                    ),
                    MessageTemplateAction(
                        label='3號信',
                        text='3號信'
                    ),
                    MessageTemplateAction(
                        label='4號信',
                        text='4號信'
                    )

                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    #else:
    if event.message.text == "科技新聞":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    buttons_template = TemplateSendMessage(
        alt_text='目錄 ',
        template=ButtonsTemplate(
            title='選擇服務',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/3Kiewj2.jpg',
            actions=[
                MessageTemplateAction(
                    label='瓶中信遊戲',
                    text='瓶中信遊戲'
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
                ),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)
if __name__ == "__main__":
    app.run()
