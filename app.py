from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('6ol/TkzOsx2Ej9mikY8+FU6SegSuiLpMWg8v9aLR+VJ/ERdnRFmEYoLQ2QCXZQb34Mhr5saLpkSH+5FeyQa3zaDekwISNXef8rq8FVSyuSAiSVFiQakv9u9PM6qq3dMrZ7YxbsxB2pyItBZaISwdRgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e73f4ba68c0127b885304278fe5fd152')

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

#----------從這裡開始複製----------

#設定帳號class
class user:
    def __init__(self,ID,Name,Situation):
        self.Name = Name
        self.ID = ID
        self.Situation = Situation

#會員系統
def GetUserList():
    url = "https://script.google.com/macros/s/AKfycbwVs2Si91yKz6m3utpaPtsttbh_lUQ8LOQM3Zud2hPFxXCgW3u1/exec"
    payload = {
        'sheetUrl':"https://docs.google.com/spreadsheets/d/1PGw2Eca9UCR8Qf_8c9_aW9X4x_Mw6SPmDgC5YgOBzX0/edit?usp=sharing",
        'sheetTag':"工作表1",
        'row': 1,
        'col': 1,
        'endRow' : 51,
        'endCol' : 20
    }
    resp = requests.get(url, params=payload)
    temp = resp.text.split(',')
    userlist = []
    i = 0
    while i < len(temp):
        if temp[i] != "":
            userlist.append(user(temp[i],temp[i+1],temp[i+2]))
            i+=3
        else:
            break
    return userlist

#登入系統
def Login(user_id,userlist):
    for user in userlist:
        if user.ID == user_id:
            return userlist.index(user)
    return -1

def Signup(user_id,name):
    url = "https://script.google.com/macros/s/AKfycbxn7Slc2_sKHTc6uEy3zmm3Bh_4duiGCXLavUM3RB0a3yzjAxc/exec"
    payload = {
        'sheetUrl':"https://docs.google.com/spreadsheets/d/1PGw2Eca9UCR8Qf_8c9_aW9X4x_Mw6SPmDgC5YgOBzX0/edit?usp=sharing",
        'sheetTag':"工作表1",
        'data':user_id+','+name+',-1'
    }
    requests.get(url, params=payload)

#寫入資料
def Write(Row,data,Col):
    url = "https://script.google.com/macros/s/AKfycbyBbQ1lsq4GSoKE0yiU5d6x0z2EseeBNZVTewWlSZhQ6EVrizo/exec"
    payload = {
        'sheetUrl':"https://docs.google.com/spreadsheets/d/1PGw2Eca9UCR8Qf_8c9_aW9X4x_Mw6SPmDgC5YgOBzX0/edit?usp=sharing",
        'sheetTag':"工作表1",
        'data':data,
        'x':str(Row+1),
        'y':str(Col)
    }
    requests.get(url, params=payload)

#關鍵字系統
def KeyWord(event):
    KeyWordDict = {"你好":"你也好啊",
                   "你是誰":"我是大帥哥",
                   "帥":"帥炸了",
                   "差不多了":"讚!!!"}

    for k in KeyWordDict.keys():
        if event.message.text.find(k) != -1:
            return [True,KeyWordDict[k]]
    return [False]

#指令系統，若觸發指令會回傳True
def Command(event):
    tempText = event.message.text.split(",")
    if tempText[0] == "發送" and event.source.user_id == "U95418ebc4fffefdd89088d6f9dabd75b":
        line_bot_api.push_message(tempText[1], TextSendMessage(text=tempText[2]))
        return True
    else:
        return False

#回應系統
def Reply(event,userlist,clientindex):
    if not Command(event):
        Ktemp = KeyWord(event)
        if Ktemp[0]:
            line_bot_api.reply_message(event.reply_token,
                TextSendMessage(text = Ktemp[1]))
        else:
            if userlist[event.source.user_id] == '-1':
                line_bot_api.reply_message(event.reply_token,
                    TextSendMessage(text = "你知道台灣最稀有、最浪漫的鳥是哪一種鳥嗎？"))
                Write(clientindex,'0',3)
            else:
                if event.message.text == "黑面琵鷺":
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text = "你居然知道答案!!!"))
                else:
                    line_bot_api.reply_message(event.reply_token,
                        TextSendMessage(text = "答案是：黑面琵鷺!!!因為每年冬天，他們都會到台灣來\"壁咚\""))
                Write(clientindex,'-1',3)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        userlist = GetUserList()
        clientindex = Login(event.source.user_id,userlist)
        if clientindex > -1:
            #開始使用功能
            line_bot_api.push_message(event.source.user_id, TextSendMessage(text=userlist[clientindex].Name))
            Reply(event,userlist,clientindex)
            '''
            line_bot_api.push_message("U95418ebc4fffefdd89088d6f9dabd75b", TextSendMessage(text=event.source.user_id + "說:"))
            line_bot_api.push_message("U95418ebc4fffefdd89088d6f9dabd75b", TextSendMessage(text=event.message.text))
            '''
        else:
            message = TemplateSendMessage(
                alt_text='確認姓名(手機限定)',
                template=ConfirmTemplate(
                    text='初次使用需要登記姓名\n您叫做'+event.message.text+'嗎?',
                    actions=[
                        PostbackTemplateAction(
                            label='對',
                            data='0`t`'+event.message.text
                        ),
                        PostbackTemplateAction(
                            label='不對',
                            data='0`f'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, 
            TextSendMessage(text=str(e)))

#處理Postback
@handler.add(PostbackEvent)
def handle_postback(event):
    userlist = GetUserList()
    clientindex = Login(event.source.user_id,userlist)
    data = event.postback.data.split('`')
    #註冊用
    if data[0] == '0' and clientindex < 0:
        if data[1] == 't':
            Signup(event.source.user_id,data[2])
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="註冊成功，歡迎來到LineBot世界"))
        elif data[1] == 'f':
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請再次輸入您的姓名"))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)