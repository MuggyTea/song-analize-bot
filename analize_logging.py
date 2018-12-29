#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ログのライブラリ
import logging
from logging import getLogger, StreamHandler, Formatter, FileHandler
from datetime import datetime
import os
import upload_s3

"""
1. loggerの設定
"""
# loggerオブジェクトの宣言
logger = getLogger('ChordAnalizeLog')
# set logging Level
logger.setLevel(logging.DEBUG)

"""
2. handlerの設定
"""

# create handler
stream_handler = StreamHandler()
# set logging format
handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)

# テキスト出力先
timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
logging_file = 'ChordAnalize_{}.log'.format(timestamp)
if os.path.exists('/tmp/analize_log/') is not True:
    os.mkdir('/tmp/analize_log/')
file_handler = FileHandler('/tmp/analize_log//{}'.format(logging_file))
# S3にアップロード
upload_s3.sign_s3('/tmp/analize_log//{}'.format(logging_file), 'log/{}'.format(logging_file))
# set logging format for log files
file_handler.setFormatter(handler_format)

"""
3. loggerにhandlerをセット
"""
# 標準出力のhandlerをセット
logger.addHandler(stream_handler)
# テキスト出力のhandlerをセット
logger.addHandler(file_handler)

"""
ログ出力テスト
"""

logger.debug('test')