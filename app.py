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
line_bot_api = LineBotApi('rPzH0qSFLM093CZwNLrEw7FbzvyZh+LzSzk6nK9LCqzag+TgDcQenMPuW9AMLvBka79K4W/IYOo0K3B9R+Zm8as0KtX1THLS2tj44eHnfkWtZNJr7JvEjPfLaNtC/q3OJBgeqqUl1X2t8ISuQifrcgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6f1bcdf89caea3506ee178e114cb3fb2')

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text = Reply(event.message.text))
    line_bot_api.reply_message(event.reply_token, message)

def Reply(text):
    if text == "hi" :
        return 'hello'

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
