#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ログのライブラリ
import logging
from logging import getLogger, StreamHandler, Formatter, FileHandler
from datetime import datetime
import os

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
timestamp = datetime.now().strftime("%Y-%m-%d")
logging_file = 'ChordAnalize_{}.log'.format(timestamp)
if os.path.exists('log/') is not True:
    os.mkdir('log/')
file_handler = FileHandler('log/{}'.format(logging_file))
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