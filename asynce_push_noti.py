#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LINE BOTは20秒間応答がないとコネクションタイムアウトする。
これを防ぐため、曲を受け取り、「解析するよー」メッセージを送った後から、
非同期で20秒ごとにpush通知を送る処理を入れる

5秒の処理がかかる関数（この関数に入ったら5秒スリープする）
2秒ごとにコールする関数を
非同期で行うイメージ
"""

import asyncio
from analize_logging import logger
import time

import mp3_to_response
import song_upload

# time_limit = 5
# このタスクが、m4a to mp3取り込みとする
tasks = [1, 3, 4, 5, 6, 7, 7, 7,3, 5, 7, 7,2 ]
index = 0
order = 'order'

async def sleeping(t, sleepingtime, hook=None):
    """
    「重いけど処理順は問わない」処理。
    重たい処理（m4aの読み込み。mp3に変換）はここで行う。
    """
    # logger.info('sleeping {} sec')
    logger.info('sleeping: {}'.format(t))
    # awaitが行われるということは何か重たい処理が始まるということ
    await asyncio.sleep(t)
    logger.info('await asyncio.sleep TASK: {}'.format(t))
    if hook:
        hook(order)
    time.sleep(sleepingtime)
    logger.info('sleeping time {} [sec]\n'.format(sleepingtime))
    return order

# 一つ目のタスク
async def basic_async(num, sleepingtime):
    """
    処理の中核
    :return:
    """
    logger.info('basic async')
    # awaitでsleeptingの処理が終わるのを待ってる
    for t in tasks:
        # これをやってる間に
        r = await sleeping(t, sleepingtime)
        logger.info('await sleeping')
        logger.info("{0}'s {1} is finished".format(num, r))
        index = +1
        logger.info('index {}'.format(index))
        # time.sleep(1)
        logger.info('basic_async time {} [sec]\n'.format(sleepingtime))
    return True
# 二つ目のタスク
async def basic_async_2(msg, sleepingtime):
    """
    処理の中核
    :return:
    """
    index = 0
    while True:
        logger.info('\nbasic async')
        r = await sleeping(msg, sleepingtime)
        logger.info('await sleeping')
        # これをやってる間に
        logger.info("SUB task count {}".format(index))
        time.sleep(sleepingtime)
        logger.info('2basic_async time {} [sec]\n'.format(sleepingtime))
        index = +1
        # return True

if __name__ == "__main__":
    # 処理の実行を担うのがこのイベントグループ。
    # これが「ノンブロッキングなスレッド」
    loop = asyncio.get_event_loop()
    logger.info('make loop')
    # ２のタスクを生成する。
    # 一つの処理がawaitに入ったら次の処理をしてを繰り返す
    # 一つ目の時間がかかるタスク。（5秒間スリープする。）
    asyncio.ensure_future(basic_async(1, 5))
    logger.info('done basic_async 1')
    # サブタスク（２秒ごとにログを吐くだけ）
    asyncio.ensure_future(basic_async_2(2222, 2))
    logger.info('done basic_async 2')
    # ２つの処理が終わるまで繰り返す
    loop.run_forever()

    # song_upload.m4a_to_mp3('tmp/幼女２ 1.m4a')