#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import traceback
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, AudioMessage
)

import settings
import chord_analize
import song_upload
import set_response

app = Flask(__name__)
# httpsでアクセスできるようにする
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('cert.crt', 'server_secret.key')


line_bot_api = LineBotApi(settings.YOUR_CHANNERL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNERL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

# 音声ファイルを受け取る関数
@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: '+str(body))
    print('Request body: ' + str(body))

    # hadle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=(TextMessage, AudioMessage))
def handle_message(event):
    # eventがRequest Body
    """
    Request body: {
        "events":
                [
                    {
                    "type":"message",
                    "replyToken":"7ba6d25051584a7ca74ac658a5bdc758",
                    "source":{
                        "userId":"Ufc78ba9ae7596cda855bc9f7e4f00498",
                        "type":"user"
                        },
                    "timestamp":1545766534620,
                    "message":{
                        "type":"text",
                        "id":"9070678793256",
                        "text":"はやか"
                        }
                    }
                ],
        "destination":"Ue5d4eb302368f469540f3742b5f6d2dc"
        }
    """
    # 入ってきたものがaudioだったら
    if event.message.type is not 'audio':
        app.logger.info('Sending Message: ' + str(event.message.text))
        print('Sending Message: ' + str(event.message.text))
        # LINE BOTが返す内容を決める
        try:
            line_bot_api.reply_message(
                event.reply_token,  # トークンとテキストで紐づけてる
                TextSendMessage(

                    text='あなたと一緒にコード解析のお手伝いするよ\n'
                         '15分以内の音楽ファイルか音声を送ってみてね')
            )
        except LineBotApiError as e:
            line_bot_api.reply_message(
                event.reply_token,  # トークンとテキストで紐づけてる
                TextSendMessage(text='error')
            )
            print(e)
        return 'ok'

    print(str(event.message.id))
    # オーディオデータ（バイナリ形式。'audio/x-m4a'）を取得する
    message_content = line_bot_api.get_message_content(event.message.id)
    # tmpディレクトリに保存
    input_file_path = 'tmp/{}.m4a'.format(event.message.id)
    with open(input_file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    try:
        # m4aバイナリファイルをローカルに保存し、mp3バイナリファイルに変換する
        chunk_mp3 = song_upload.m4a_to_mp3(input_file_path, open(input_file_path, 'rb'))
        # mp3を引数にして、コード解析APIに投げる
        analize_chord = chord_analize.detect_chords(input_file=chunk_mp3)
        app.logger.info('Sending Message: ' + str(analize_chord))
        print('Sending Message: ' + str(analize_chord))
        # 得られたレスポンスを成形する
        num_chords, chord_analize_response = set_response.set_response_chord_analize(analize_chord)
    except:
        print(traceback.format_exc())
        raise

    try:
        # # LINE BOTが返す内容を決めるメソッド
        # line_bot_api.reply_message(
        #     event.reply_token,  # トークンとテキストで紐づけてる
        #     TextSendMessage(text=analize_chord)
        # )
        # LINE BOTが返す内容を決めるメソッド
        line_bot_api.reply_message(
            event.reply_token,  # トークンとテキストで紐づけてる
            TextSendMessage(
                text=
                str(chord_analize_response)
            )
        )

        print(analize_chord)
    except LineBotApiError as e:
        line_bot_api.reply_message(
            event.reply_token,  # トークンとテキストで紐づけてる
            TextSendMessage(text='レスポンス文字列が長すぎるのでちょっと待ってね')
        )
        print(e)
    return 'ok'

if __name__ == '__main__':
    port = os.environ.get('PORT', 3333)
    # app.run(
    #     host = 'localhost',port=3333, ssl_context=context, threaded=True, debug=True
    # )
    app.run(
        host = 'localhost',port=3333
    )