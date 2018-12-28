
import chord_analize
import set_response
from analize_logging import logger

import json

""" mp3データを解析して、レスポンスを成形する関数 """
def mp3_to_response(data_mp3):
    logger.info('Do analizing mp3 data: {}'.format(data_mp3))
    # mp3を引数にして、コード解析APIに投げる
    analize_chord = chord_analize.detect_chords(input_file=data_mp3)
    # str型なので、JSON形式に変換する
    analize_chord_j = json.loads(analize_chord)
    logger.info('Response Header: {}'.format(analize_chord))
    if analize_chord_j['status']['code'] == (200 or 201):
        # 得られたレスポンスを成形する
        chord_analize_response = set_response.set_response_chord_analize(analize_chord)
        logger.info('Made Response:{} '.format(str(chord_analize_response)))
        return chord_analize_response
    elif analize_chord_j['errors']:
        if analize_chord_j['errors'][0]['error_code'] == '23':
            chord_analize_response = 'オーディオファイルが短すぎるみたい。\n15秒以上にしてもう一回送ってみてね！'
            logger.info('Made Response: '.format(chord_analize_response))
            return chord_analize_response
        elif analize_chord_j['errors'][0]['error_code'] == '22':
            chord_analize_response = '私の知らないファイル形式かも。\n' \
                                     'mp3形式かaac形式しか今はわからないんだ、、。\nあなたは物知りで凄いなぁ'
            logger.info('Made Response: '.format(chord_analize_response))
            return chord_analize_response
        else:
            chord_analize_response = 'ちょっと調子が悪いみたい。\nもう一回試してみてもらえるかな？'
            logger.info('Made Response: '.format(chord_analize_response))
            return chord_analize_response