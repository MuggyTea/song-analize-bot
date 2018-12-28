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
MAX_RETRY = 6

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
    # 入ってきたものがaudio以外だったら、デフォルトメッセージを返す
    if event.message.type is not 'audio':
        start_youtube_time = time.time()
        if 'https://www.youtube.com/' in event.message.text:
            logger.info('Message ID: {}'.format(str(event.message.id)))
            logger.info('User ID: {}'.format(str(event.source.user_id)))
            logger.info('been Sent Message: ' + str(event.message.text))
            print('been Sent Message: ' + str(event.message.text))
            # youtubeURLの場合はmp3解析する(userIdにrenameする)
            # 10秒以内に応答がないとセッションタイムアウトになるので、送る
            line_bot_api.push_message(
                event.source.user_id,  # トークンとテキストで紐づけてる
                TextSendMessage(
                    text='解析してみる！\n'
                         '2分くらいでできたら良いなあ\n'
                         '終わったらまた話しかけるねー'
                )
            )
            yt2mp4 = youtube2mp3(event.message.text, event.message.id)
            logger.info('get youtube mp4 data. {}'.format(yt2mp4))
            yt2mp3 = song_upload.m4a_to_mp3(yt2mp4)
            # 得られたmp3データからレスポンス成形
            chord_analize_response = mp3_to_response(yt2mp3)
            for i in range(1, MAX_RETRY):
                try:
                    logger.info('Result: {}'.format(chord_analize_response))
                    # LINE BOTが返す内容を決めるメソッド
                    end_youtube_time = time.time() - start_youtube_time
                    logger.info('time for analize youtube audio: {}'.format(
                        end_youtube_time))
                    line_bot_api.push_message(
                        event.source.user_id,  # トークンとテキストで紐づけてる
                        TextSendMessage(
                            text=
                            str(chord_analize_response)
                        )
                    )
                    logger.info('Success! Sent response for user: {}'.format(chord_analize_response))
                    break
                except LineBotApiError as e:
                    logger.error('LineBotApiError: {}'.format(traceback.format_exc()))
                    logger.error('retry: {0}/{1}'.format(i, MAX_RETRY-1))
                    sleep(i*5)
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
        for i in range(1, MAX_RETRY):
            try:
                line_bot_api.reply_message(
                    event.reply_token,  # トークンとテキストで紐づけてる
                    TextSendMessage(
                        text='あなたと一緒にコード解析するよー！\n'
                             '5分以内のmp3音楽ファイルか音声を録音して送ってみてね'
                             )
                )
                break
            except LineBotApiError as e:
                logger.error('LineBotApiError: {}'.format(e))
                logger.error('retry: {0}/{1}'.format(i, MAX_RETRY))
                line_bot_api.reply_message(
                    event.reply_token,  # トークンとテキストで紐づけてる
                    TextSendMessage(text='あなたと一緒にコード解析するよー！\n'
                                         '10分以内の音楽ファイルか音声を録音して送ってみてね\n')
                )
                
        return 'ok'
        """

    start_time = time.time()
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
    # 10秒以内に応答がないとセッションタイムアウトになるので、送る
    line_bot_api.push_message(
        event.source.user_id,  # トークンとテキストで紐づけてる
        TextSendMessage(
            text='解析してみる！\n30秒後くらいにまた話しかけるねー'
        )
    )
    with open(input_file_path, 'wb') as fd:
        for i in range(MAX_RETRY):
            try:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
                break
            except:
                logger.error('LineBotApiError: {}'.format(traceback.format_exc()))
                logger.error('retry: {0}/{1}'.format(i, MAX_RETRY))
                sleep(i * 5)
        # S3にアップロード
        upload_s3.sign_s3(input_file_path, 'm4a/{}.m4a'.format(event.message.id))
    # m4aバイナリファイルをローカルに保存し、mp3バイナリファイルに変換する
    chunk_mp3 = song_upload.m4a_to_mp3(input_file_path)
    chord_analize_response = mp3_to_response(chunk_mp3)
    for i in range(1, MAX_RETRY):
        try:
            end_time = time.time() - start_time
            logger.info('Elapsed time: {} [sec]'.format(end_time))
            # １レスポンス後30秒開ける必要があるため、30秒経つまでまでスリープする
            # if end_time > 30:
            #     logger.info('sleeping {} [sec]'.format(30-end_time))
            #     sleep((30-end_time))
            # logger.info('Result: {}'.format(chord_analize_response))
            # LINE BOTが返す内容を決めるメソッド
            """push API使えないバージョン
            line_bot_api.reply_message(
                event.reply_token,  # トークンとテキストで紐づけてる
                TextSendMessage(
                    text=
                    str(chord_analize_response)
                )
            )
            """
            # push APIで送る
            line_bot_api.push_message(
                event.source.user_id,  # トークンとテキストで紐づけてる
                TextSendMessage(
                    text=
                    str(chord_analize_response)
                )
            )
            logger.info('Success! Sent response for user: {}'.format(chord_analize_response))
            break
        except LineBotApiError as e:
            logger.error('LineBotApiError: {}'.format(traceback.format_exc()))
            logger.error('retry: {0}/{1}'.format(i, MAX_RETRY-1))
            sleep(i*5)
    return 'ok'


if __name__ == '__main__':
    app.run(
        host = 'localhost',port=3333
    )
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)