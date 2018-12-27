#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import traceback
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError)
from linebot.models import (
    MessageEvent,  TextSendMessage,
    TextMessage, AudioMessage,
    FileMessage,ImageMessage, StickerMessage, VideoMessage, LocationMessage,
)

import settings
import upload_s3
import chord_analize
import song_upload
import set_response
from analize_logging import logger
from youtube2mp3 import youtube2mp3
from mp3_to_response import mp3_to_response
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
    logger.info('Request body: '+str(body))
    print('Request body: ' + str(body))

    # hadle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=(TextMessage, AudioMessage,
                                    FileMessage,ImageMessage,
                                    StickerMessage, VideoMessage, LocationMessage))
def handle_message(event):
    try:
        # 入ってきたものがaudio以外だったら、デフォルトメッセージを返す
        if event.message.type is not 'audio':
            """
            if 'https://www.youtube.com/' in event.message.text:
                try:
                    logger.info('Message ID: {}'.format(str(event.message.id)))
                    logger.info('been Sent Message: ' + str(event.message.text))
                    print('been Sent Message: ' + str(event.message.text))
                    # youtubeURLの場合はmp3解析する(userIdにrenameする)
                    yt2mp4 = youtube2mp3(event.message.text, event.message.id)
                    logger.info('get youtube mp4 data. {}'.format(yt2mp4))
                    yt2mp3 = song_upload.m4a_to_mp3(yt2mp4)
                    # 得られたmp3データからレスポンス成形
                    chord_analize_response = mp3_to_response(yt2mp3)
                    # LINE BOTが返す内容を決めるメソッド
                    line_bot_api.reply_message(
                        event.reply_token,  # トークンとテキストで紐づけてる
                        TextSendMessage(
                            text=
                            str(chord_analize_response)
                        )
                    )
                    logger.info('Result: {}'.format(chord_analize_response))
                    return 'ok'
                except LineBotApiError as e:
                    line_bot_api.reply_message(
                        event.reply_token,  # トークンとテキストで紐づけてる
                        TextSendMessage(text='調子が悪いみたい。もう一度試してみてね')
                    )
                    logger.error(e)
                    print(e)

                    return 'ok'
            else:   # それ以外はデフォルトメッセージを返す
                # LINE BOTが返す内容を決める
                try:
                    line_bot_api.reply_message(
                        event.reply_token,  # トークンとテキストで紐づけてる
                        TextSendMessage(
                            text='あなたと一緒にコード解析するよー！\n'
                                 '5分以内のmp3音楽ファイルか音声を録音して送ってみてね\n'
                                 'youtubeのURLも調べられるよ。でも少し時間が掛かっちゃうかも')
                    )
                except LineBotApiError as e:
                    line_bot_api.reply_message(
                        event.reply_token,  # トークンとテキストで紐づけてる
                        TextSendMessage(text='あなたと一緒にコード解析するよー！\n'
                                 '10分以内の音楽ファイルか音声を録音して送ってみてね\n')
                    )
                    logger.error(e)
                    print(e)
                return 'ok'
            """
            try:
                line_bot_api.reply_message(
                    event.reply_token,  # トークンとテキストで紐づけてる
                    TextSendMessage(
                        text='あなたと一緒にコード解析するよー！\n'
                             '5分以内のmp3音楽ファイルか音声を録音して送ってみてね'
                             )
                )
            except LineBotApiError as e:
                line_bot_api.reply_message(
                    event.reply_token,  # トークンとテキストで紐づけてる
                    TextSendMessage(text='あなたと一緒にコード解析するよー！\n'
                                         '10分以内の音楽ファイルか音声を録音して送ってみてね\n')
                )
                logger.error(e)
                print(e)
            return 'ok'

        # print(str(event.message.id))
        logger.info('Message ID: {}'.format(str(event.message.id)))
        # オーディオデータ（バイナリ形式。'audio/x-m4a'）を取得する
        message_content = line_bot_api.get_message_content(event.message.id)
        # tmpディレクトリに保存
        input_file_path = '/tmp/{}.m4a'.format(event.message.id)
        logger.info('Receive m4a file name: {}'.format(str(input_file_path)))
        if os.path.exists('/tmp/') is not True:
            logger.info('make temporary directory')
            os.mkdir('/tmp/')
        with open(input_file_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        # m4aバイナリファイルをローカルに保存し、mp3バイナリファイルに変換する
        # chunk_mp3 = song_upload.m4a_to_mp3(input_file_path, open(input_file_path, 'rb'))
        chunk_mp3 = song_upload.m4a_to_mp3(input_file_path)
        chord_analize_response = mp3_to_response(chunk_mp3)

        # LINE BOTが返す内容を決めるメソッド
        line_bot_api.reply_message(
            event.reply_token,  # トークンとテキストで紐づけてる
            TextSendMessage(
                text=
                str(chord_analize_response)
            )
        )
        logger.info('Result: {}'.format(chord_analize_response))
    except LineBotApiError as e:
        logger.error(e)
        print(e)
        line_bot_api.reply_message(
            event.reply_token,  # トークンとテキストで紐づけてる
            TextSendMessage(text='調子が悪いみたい。もう一度試してみてね')
        )
    return 'ok'


if __name__ == '__main__':
    app.run(
        host = 'localhost',port=3333
    )
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)