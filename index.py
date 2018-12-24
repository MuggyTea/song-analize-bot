#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNERL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNERL_SECRET')

@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: '+str(body))

    # hadle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextSendMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = event.message.text)
    )

if __name__ == '__main__':
    port = os.environ.get('PORT', 3333)
    app.run()