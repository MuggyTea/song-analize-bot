#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from analize_logging import logger

""" コード解析して得られた結果を成形する関数 """
def set_response_chord_analize(analize_chord_s):
    """
    レスポンスの形
    {
        "status":{
            "code":200
            },
        "chords_result":{
            "num_chords":13,
            "chords":[
                {
                    "index":0,
                    "time":0.18693749606609344,
                    "chord":"C#:maj7"
                },
                {
                    "index":1,
                    "time":0.8999375104904175,
                    "chord":"F:7"
                },
                {
                "index":2,
                "time":1.973312497138977,
                "chord":"F#:maj7"
                },
            ]
        }
    }

    :param analize_chord:
    :return: chord_analize_response
    """
    # str型を辞書型に変換
    analize_chord_j = json.loads(analize_chord_s)
    logger.info('str count of result'.format(len(str(analize_chord_s))))
    # 総検出数
    num_chords = analize_chord_j['chords_result']['num_chords']
    # コードのみを格納する辞書を用意する
    chords_list = []
    # 取りたい項目を決める（今回は'chords'）
    for key, value in enumerate(analize_chord_j['chords_result']['chords']):
        # コードのみ抽出
        chord = value['chord']
        # リストに格納
        chords_list.append(chord)

    return num_chords, chords_list