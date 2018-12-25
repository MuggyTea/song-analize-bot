#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as r

import settings

"""
Sonic APIのコード解析APIを取得するところまで担当する
"""
KEY1 = settings.SONIC_API_KEY


def set_param_to_api(endpoint, input_file_path):
    # Detect chords api endpoint
    url = 'https://api.sonicAPI.com/{0}?access_id={1}'.format(endpoint, KEY1)
    datas = {
        'format': 'json'
    }
    # files = {'input_file': (input_file, 'file')}
    input_file = open(input_file_path, 'rb')
    files = {'input_file': input_file}

    return url, datas, files

def detect_chords_by_sonic(input_file):
    """ 音声データからコードを取得する """
    endpoint = 'analyze/chords'
    # 必要なパラメータをセットする
    url, datas, files = set_param_to_api(endpoint, input_file)
    # Sonic APIに音声データを投げる
    res = r.post(url=url, data=datas, files=files, verify=False)

    return res.text


if __name__ == "__main__":
    a = detect_chords_by_sonic(input_file='tmp/sample1.mp3')
    print(a)