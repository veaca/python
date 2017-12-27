import os , json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('4ksfjWNXRxXN3fElzCnJkfBrLBr+YZExAkxDnCHPaSjy9CZBswHJyxtqJuK7OF1HAwZUYYMHo2ynCZetDOKKHrQ03chyHrMkYK2lVv44kOXo1Copj4Yrz7MtnO3o15ttq/sVxNSRSlJuO6wvKcXLswdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('eaea5d768a94368365a2de5966999a68')


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
def handle_text_message(event):
    text = event.message.text

        if text == 'halo' :
            line_bot_api.reply_message(event.reply_token, TextMessage(text = 'hai'))
        else :
            line_bot_api.reply_message(reply_token, TextMessage(text=msgtext))
    
   

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
