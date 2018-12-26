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

"""
LIN　BOTから送信された音声データをmp3に変換し、tmp/配下にアップロードするところまで担当する
"""
KEY1 = settings.SONIC_API_KEY

# 音声ファイルをmp3に変換
def m4a_to_mp3(input_file_path, file_m4a):
    # if input_file_name.endswith('.m4a'):
    #         subprocess.call([
    #             "ffmpeg", "-i",
    #             os.path.join(path, filename),
    #             "-acodec", "libmp3lame", "-ab", "256k",
    #             os.path.join(OUTPUT_DIR, '%s.mp3' % filename[:-4])
    #         ])

    # パスから、拡張子と名前を分ける
    root, ext = os.path.splitext(input_file_path)
    if ext not in ['.m4a', '.mp4']:
        print('if ext not in m4a')
        return
    # 変換するmp3ファイルの名前
    input_file_path_mp3 = '%s.mp3' % root
    # m4a to mp3（どちらもバイナリではなくパスを指定すること）
    cmd = 'ffmpeg -i %s %s' % (input_file_path, input_file_path_mp3)
    status, output = subprocess.getstatusoutput(cmd)
    # with open(input_file_path_mp3, mode='wb') as fb:   # ファイル名

    if status != 0:
        print('status error')
        return

    return input_file_path_mp3


if __name__ == "__main__":
    reply_token = 'dummy'
    input_file_name = 'sample22wwwwww.mp3'
    m4a_to_mp3(reply_token, input_file_name)