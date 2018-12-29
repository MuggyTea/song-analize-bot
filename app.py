#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import traceback
from time import sleep
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError
)
from linebot.models import (
    MessageEvent,  TextSendMessage,
    TextMessage, AudioMessage,
    FileMessage,ImageMessage, StickerMessage, VideoMessage, LocationMessage,
)

from pydub import AudioSegment
import settings
import upload_s3
import chord_analize
import song_upload
import set_response
from analize_logging import logger, logging_file
from youtube2mp3 import youtube2mp3
from mp3_to_response import mp3_to_response
import asyncio
app = Flask(__name__)
# httpsでアクセスできるようにする
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('cert.crt', 'server_secret.key')


line_bot_api = LineBotApi(settings.YOUR_CHANNERL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNERL_SECRET)
MAX_RETRY = 6

@app.route("/")
def hello_world():
    return "hello world!"

# asyncとつけると通常の関数ではなくコルーチン
async def wrap_with_delay(sec, func, *args):
    await asyncio.sleep(sec) # awaitで制御をイベントループにもどす
    func(*args)

def check_timeout(push, loop=None):
    logger.info('check timeout')
    if loop is None:
        loop = asyncio.get_event_loop()
        loop.stop()  # イベントループをとめて制御をもどす処理を追加

# 音声ファイルを受け取る関数
@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    logger.info('Request body: '+str(body))
    upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'log/{}'.format(logging_file))
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
    if event.message.type is not 'audio':
    # 入ってきたものがaudio以外だったら、デフォルトメッセージを返す
        start_youtube_time = time.time()
        for i in range(1, MAX_RETRY):
            try:
                line_bot_api.reply_message(
                    event.reply_token,  # トークンとテキストで紐づけてる
                    TextSendMessage(
                        text='あなたと一緒にコード解析するよー！\n'
                             'LINEで録音して送ってみてね。\n'
                             '容量の小さいmp3ファイルも解析できるよ'
                             )
                )
                break
            except LineBotApiError as e:
                logger.error('LineBotApiError: {}'.format(e))
                logger.error('retry: {0}/{1}'.format(i, MAX_RETRY))
                line_bot_api.reply_message(
                    event.reply_token,  # トークンとテキストで紐づけてる
                    TextSendMessage(text='あなたと一緒にコード解析するよー！\n'
                                         'LINEで録音して送ってみてね\n'
                                         '容量の小さいmp3ファイルも解析できるよ\n')
                )
                
        return 'ok'
    logger.info('Message ID: {}'.format(str(event.message.id)))
    upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'log/{}'.format(logging_file))
    # オーディオデータ（バイナリ形式。'audio/x-m4a'）を取得する
    message_content = line_bot_api.get_message_content(event.message.id)
    # tmpディレクトリに保存
    input_file_path = '/tmp/{}.m4a'.format(event.message.id)
    logger.info('Receive m4a file name: {}'.format(str(input_file_path)))
    upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'log/{}'.format(logging_file))
    if os.path.exists('/tmp/') is not True:
        logger.info('make temporary directory')
        os.mkdir('/tmp/')

    line_bot_api.push_message(
        event.source.user_id,  # トークンとテキストで紐づけてる
        TextSendMessage(text='解析してみるよー！\n'
                             '終わったら話しかけるねー。\n'
                             '1分経ってもお返事が来なかったら、もう少し短いファイルを送ってみてくれるかな？')
    )
    start_chunk = time.time()
    with open(input_file_path, 'wb') as fd:
        for i in range(MAX_RETRY):  # m4aバイナリの書き込みに失敗したら、5回までリトライ処理入れる
            try:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
                break
            except:
                logger.error('LineBotApiError: {}'.format(traceback.format_exc()))
                logger.error('retry: {0}/{1}'.format(i, MAX_RETRY))
                sleep(i * 5)
        end_chunk = time.time() - start_chunk
        logger.info('chunk time: {}'.format(end_chunk))
        start_conv_mp3 = time.time()
        # S3にアップロード
        upload_s3.sign_s3(input_file_path, 'm4a/{}.m4a'.format(event.message.id))

    # m4aバイナリファイルをローカルに保存し、mp3バイナリファイルに変換する
    chunk_mp3 = song_upload.m4a_to_mp3(input_file_path)
    end_conv_mp3 = time.time() - start_conv_mp3
    logger.info('converted time: {} [sec]'.format(end_conv_mp3))
    start_analize = time.time()
    chord_analize_response = mp3_to_response(chunk_mp3)
    end_analize = time.time() - start_analize
    logger.info('Analize time: {} [sec]'.format(end_analize))
    # push API使えないバージョン
    # line_bot_api.reply_message(
    #     event.reply_token,  # トークンとテキストで紐づけてる
    #     TextSendMessage(
    #         text=
    #         str(chord_analize_response)
    #     )
    # )
    line_bot_api.push_message(
        event.source.user_id,  # トークンとテキストで紐づけてる
        TextSendMessage(text=str(chord_analize_response))
    )
    logger.info('Success! Sent response for user: {}'.format(chord_analize_response))
    # S3にアップロード
    upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'log/{}'.format(logging_file))
    return 'ok'


if __name__ == '__main__':
    app.run(
        host = 'localhost',
        port=3333,
        threaded=True
    )