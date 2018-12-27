#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as r

import settings
import subprocess
import os
import os.path

# !/usr/bin/env python
import sys
import os
import glob
from analize_logging import logger

"""
LIN　BOTから送信された音声データをmp3に変換し、tmp/配下にアップロードするところまで担当する
"""
KEY1 = settings.SONIC_API_KEY

# 音声ファイルをmp3に変換
def m4a_to_mp3(input_file_path, file_m4a):
    # パスから、拡張子と名前を分ける
    root, ext = os.path.splitext(input_file_path)
    if ext not in ['.m4a', '.mp4']:
        print('if ext not in m4a')
        logger.debug('input file: {}'.format(str(input_file_path)))
        return
    # 変換するmp3ファイルの名前
    input_file_path_mp3 = '%s.mp3' % root
    # set commands for m4a to mp3 using ffmpeg
    cmd = 'ffmpeg -i %s %s' % (input_file_path, input_file_path_mp3)
    logger.info('converted mp3 file: {}'.format(input_file_path_mp3))
    # do m4a to mp3（どちらもバイナリではなくパスを指定すること）
    status, output = subprocess.getstatusoutput(cmd)

    if status != 0:
        print('status error')
        logger.error('failed convert {0}, {1}'.format(status, output))
        return
    # mp3ファイルパスを返す
    return input_file_path_mp3


if __name__ == "__main__":
    reply_token = 'dummy'
    input_file_name = 'sample22wwwwww.mp3'
    m4a_to_mp3(reply_token, input_file_name)