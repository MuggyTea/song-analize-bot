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

# time_limit = 5
task = [1, 3, 4, 5, 6, 7, 7, 7,3, 5, 7, 7,2 ]
index = 0
order = 'order'

async def sleeping(order, time_limit, hook=None):
    """
    「重いけど処理順は問わない」処理。
    重たい処理（m4aの読み込み。mp3に変換）はここで行う。
    """
    logger.info('sleeping 10sec')
    # awaitが行われるということは何か重たい処理が始まるということ
    await asyncio.sleep(time_limit)
    logger.info('await asyncio.sleep')
    if hook:
        hook(order)
    a = time.sleep(2)
    logger.info('sleeping time {} [sec]\n'.format(2))
    return order

async def basic_async(num, sleepingtime):
    """
    処理の中核
    :return:
    """
    logger.info('basic async')
    # awaitでsleeptingの処理が終わるのを待ってる
    for t in task:
        r = await sleeping(order, t)
        logger.info('await sleeping')
        logger.info("{0}'s {1} is finished".format(num, r))
        index = +1
        logger.info('index {}'.format(index))
        time.sleep(5)
        logger.info('basic_async time {} [sec]\n'.format(sleepingtime))
    return True

if __name__ == "__main__":
    # 処理の実行を担うのがこのイベントグループ。
    # これが「ノンブロッキングなスレッド」
    loop = asyncio.get_event_loop()
    logger.info('make loop')
    # ２のタスクを生成する。
    # 一つの処理がawaitに入ったら次の処理をしてを繰り返す
    # while True:
    asyncio.ensure_future(basic_async(1, 2))
    logger.info('done basic_async 1')
    asyncio.ensure_future(basic_async(2, 5))
    logger.info('done basic_async 2')
    # ２つの処理が終わるまで繰り返す
    loop.run_forever()