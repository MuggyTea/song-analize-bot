#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pytube import YouTube
from analize_logging import logger
import os
from pydub import AudioSegment

def youtube2mp3(youtube_url, line_userid):
    logger.info('youtube url: {}'.format(youtube_url))
    print('youtube url: {}'.format(youtube_url))
    # youtube動画を抜き出す
    yt = YouTube(youtube_url)
    # 動画の情報を出力
    for lis in yt.streams.all():
        logger.info(lis)
    # get_bu_itagtodownloadメソッドででダウンロードができる
    yt2mp3 = yt.streams.get_by_itag(140).download('tmp/')
    print(yt2mp3)
    logger.info('youtube video converted to mp4 {}'.format(yt2mp3))
    # LINEのuseridにrenameする
    input_file_path = '/tmp/{}.mp4'.format(line_userid)
    os.rename(yt2mp3, input_file_path)
    # mp3ファイルを5分にカットする
    mp4 = AudioSegment.from_file(input_file_path, format='mp4')
    # 0~500sec(300000ms)にカット
    mp4_1min = mp4[0:60000]
    # logger.info('rename: {}'.format(os.rename(yt2mp3, 'tmp/{}.mp4'.format(line_userid))))
    logger.info('Receive mp4 file name: {}'.format(input_file_path))
    # with open(yt2mp3, 'wb') as fb:
    #     fb.write(yt2mp3)

    return input_file_path

if __name__ == "__main__":
    line_userid = '123456eafr7'
    youtube_url = 'https://www.youtube.com/watch?v=O6qFWp4auX4'
    youtube2mp3(youtube_url, line_userid)