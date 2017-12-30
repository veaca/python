import os , json, requests

from bs4 import BeautifulSoup as soup

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
def handle_message(event):
    simpan = json.loads(str(event))
    txtpesan = simpan['message']['text']
    reply_token = simpan['replyToken']
    if txtpesan.lower() == 'show' :
        textSimpan=json.dumps(simpan,indent=2)
        line_bot_api.reply_message(reply_token, TextSendMessage(text=textSimpan))
    if txtpesan.lower() == 'coba' :
        url = 'https://en.wikipedia.org/wiki/Indonesia'
        page = requests.get(url)
        #page_soup = soup(page.text, 'html.parser')
        #tampil = str(page_soup)
        line_bot_api.reply_message(reply_token, TextSendMessage(text = str(page.status_code)))
    elif txtpesan.lower() == 'leave' :
        jenis = simpan['source']['type']
        if jenis.lower() == 'room':
            room_id = simpan['source']['roomId']
            line_bot_api.leave_room(room_id)
        elif jenis.lower() == 'group':
            group_id = simpan['source']['groupId']
            line_bot_api.leave_group(group_id)
    else :
        line_bot_api.reply_message(reply_token, TextSendMessage(text = txtpesan))
    
   

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
