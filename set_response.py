#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from analize_logging import logger

""" コード解析して得られた結果を成形する関数 """
def set_response_chord_analize(analize_chord_s):
    """
    :param analize_chord:
    :return: chord_analize_response
    """
    logger.info('Do make for response: {}'.format(analize_chord_s))
    # str型を辞書型に変換
    analize_chord_j = json.loads(analize_chord_s)
    logger.info('str count of result'.format(len(str(analize_chord_s))))
    # 総検出数
    num_chords = analize_chord_j['chords_result']['num_chords']
    # コードのみを格納する辞書を用意する
    chords_list = []
    # 取りたい項目を決める（今回は'chords'）
    for key, value in enumerate(analize_chord_j['chords_result']['chords']):
        if value['chord'] == 'N':
            continue
        # コードのみ抽出
        chord = value['chord']
        # リストに格納
        chords_list.append(chord)
    logger.info('Result Analized number of chord: {0}, Chord Progression{1}'.format(num_chords, chords_list))
    logger.info('number of string count in Response: {}'.format(len(str(chords_list))))
    if len(str(chords_list)) > 2000:
        chords_list = str(chords_list)[0:1999]

    return chords_list


if __name__ == "__main__":
    # レスポンスの形
    result ={"status":{"code":200},"chords_result":{"num_chords":108,"chords":[{"index":0,"time":0.1875963658094406,"chord":"N"},{"index":1,"time":15.623605728149414,"chord":"D#:min7"},{"index":2,"time":17.04485321044922,"chord":"F#:maj7"},{"index":3,"time":21.282516479492188,"chord":"G#:min"},{"index":4,"time":22.69510269165039,"chord":"F#:maj"},{"index":5,"time":24.10839080810547,"chord":"F:maj"},{"index":6,"time":25.488956451416016,"chord":"A#:maj"},{"index":7,"time":26.79730224609375,"chord":"D#:min7"},{"index":8,"time":28.38843536376953,"chord":"F#:maj7"},{"index":9,"time":32.530250549316406,"chord":"G#:min7"},{"index":10,"time":34.12140655517578,"chord":"F#:maj"},{"index":11,"time":35.405555725097656,"chord":"F:maj"},{"index":12,"time":36.063377380371094,"chord":"C#:maj7"},{"index":13,"time":36.71199417114258,"chord":"D#:min"},{"index":14,"time":37.97816467285156,"chord":"D:min"},{"index":15,"time":48.743309020996094,"chord":"N"},{"index":16,"time":50.609886169433594,"chord":"C:maj6"},{"index":17,"time":51.84120178222656,"chord":"B:min7"},{"index":18,"time":53.07047653198242,"chord":"E:maj"},{"index":19,"time":55.536643981933594,"chord":"C:maj6"},{"index":20,"time":56.766780853271484,"chord":"B:min7"},{"index":21,"time":58.00249481201172,"chord":"E:maj"},{"index":22,"time":59.84691619873047,"chord":"C:maj7"},{"index":23,"time":61.68898010253906,"chord":"D:maj6"},{"index":24,"time":64.15357971191406,"chord":"E:maj"},{"index":25,"time":65.38111114501953,"chord":"C:maj"},{"index":26,"time":66.6108169555664,"chord":"D:maj"},{"index":27,"time":67.8353500366211,"chord":"E:min"},{"index":28,"time":70.3000259399414,"chord":"D#:maj7"},{"index":29,"time":71.53707122802734,"chord":"D:min"},{"index":30,"time":72.7697982788086,"chord":"G:maj"},{"index":31,"time":75.23689270019531,"chord":"D#:maj7"},{"index":32,"time":76.46825408935547,"chord":"D:min"},{"index":33,"time":77.69732666015625,"chord":"G:7"},{"index":34,"time":79.84630584716797,"chord":"D#:maj7"},{"index":35,"time":81.37646484375,"chord":"F:maj6"},{"index":36,"time":82.60011291503906,"chord":"D:min"},{"index":37,"time":83.83541870117188,"chord":"G:min"},{"index":38,"time":85.07135772705078,"chord":"D#:maj"},{"index":39,"time":86.3012466430664,"chord":"F:maj"},{"index":40,"time":87.53015899658203,"chord":"G:min"},{"index":41,"time":89.99163055419922,"chord":"D#:maj7"},{"index":42,"time":91.22065734863281,"chord":"D:min"},{"index":43,"time":92.45301818847656,"chord":"G:maj"},{"index":44,"time":94.92086029052734,"chord":"D#:maj7"},{"index":45,"time":96.15140533447266,"chord":"D:min"},{"index":46,"time":97.38417053222656,"chord":"G:maj"},{"index":47,"time":99.2331314086914,"chord":"A#:maj"},{"index":48,"time":99.8477783203125,"chord":"D#:maj7"},{"index":49,"time":101.07564544677734,"chord":"F:maj7"},{"index":50,"time":102.29566955566406,"chord":"B:7"},{"index":51,"time":102.91088104248047,"chord":"N"},{"index":52,"time":104.13752746582031,"chord":"C#:min7"},{"index":53,"time":106.56330871582031,"chord":"E:maj"},{"index":54,"time":108.97095489501953,"chord":"A:maj7"},{"index":55,"time":110.16521453857422,"chord":"G#:min"},{"index":56,"time":111.35818481445312,"chord":"F#:7"},{"index":57,"time":112.55551147460938,"chord":"G#:min"},{"index":58,"time":113.75303649902344,"chord":"C#:min"},{"index":59,"time":116.15394592285156,"chord":"E:maj7"},{"index":60,"time":118.55317687988281,"chord":"A:maj"},{"index":61,"time":119.7547607421875,"chord":"G#:maj"},{"index":62,"time":120.95582580566406,"chord":"F#:min7"},{"index":63,"time":122.15821075439453,"chord":"E:7"},{"index":64,"time":122.7582778930664,"chord":"D#:min"},{"index":65,"time":123.35872650146484,"chord":"E:min"},{"index":66,"time":127.54882049560547,"chord":"D:maj6"},{"index":67,"time":128.148681640625,"chord":"C:maj7"},{"index":68,"time":130.54986572265625,"chord":"D:7"},{"index":69,"time":132.9558563232422,"chord":"E:min"},{"index":70,"time":135.36033630371094,"chord":"N"},{"index":71,"time":137.47482299804688,"chord":"F#:maj7"},{"index":72,"time":138.97421264648438,"chord":"G#:maj6"},{"index":73,"time":140.46754455566406,"chord":"F#:maj7"},{"index":74,"time":141.365966796875,"chord":"C#:maj"},{"index":75,"time":141.9630584716797,"chord":"D#:maj7"},{"index":76,"time":142.8663330078125,"chord":"F:maj"},{"index":77,"time":143.4595489501953,"chord":"F#:maj7"},{"index":78,"time":144.924560546875,"chord":"G#:maj"},{"index":79,"time":145.79563903808594,"chord":"C#:maj7"},{"index":80,"time":146.6724090576172,"chord":"F#:maj7"},{"index":81,"time":147.2676239013672,"chord":"G#:maj6"},{"index":82,"time":148.1687469482422,"chord":"A#:min"},{"index":83,"time":149.64988708496094,"chord":"N"},{"index":84,"time":151.14134216308594,"chord":"C#:min"},{"index":85,"time":152.66151428222656,"chord":"G#:min"},{"index":86,"time":154.17507934570312,"chord":"A:maj"},{"index":87,"time":155.6700897216797,"chord":"E:maj6"},{"index":88,"time":157.20091247558594,"chord":"F#:min"},{"index":89,"time":158.4212188720703,"chord":"E:maj7"},{"index":90,"time":160.19407653808594,"chord":"D#:maj"},{"index":91,"time":161.70480346679688,"chord":"G#:maj"},{"index":92,"time":162.96322631835938,"chord":"C#:maj"},{"index":93,"time":164.558349609375,"chord":"G#:maj"},{"index":94,"time":166.0722198486328,"chord":"A:maj"},{"index":95,"time":166.67750549316406,"chord":"E:maj7"},{"index":96,"time":169.174560546875,"chord":"F#:min"},{"index":97,"time":170.41879272460938,"chord":"G#:min7"},{"index":98,"time":172.00010681152344,"chord":"A:maj7"},{"index":99,"time":172.9347381591797,"chord":"B:min7"},{"index":100,"time":173.55494689941406,"chord":"C#:maj"},{"index":101,"time":176.31951904296875,"chord":"G#:min6"},{"index":102,"time":178.17140197753906,"chord":"A:maj6"},{"index":103,"time":179.7062530517578,"chord":"E:maj7"},{"index":104,"time":181.18878173828125,"chord":"F#:min6"},{"index":105,"time":182.39047241210938,"chord":"E:maj6"},{"index":106,"time":184.19309997558594,"chord":"D#:maj7"},{"index":107,"time":185.39340209960938,"chord":"N"}]}}
    analize_chord_s = json.dumps(result)

    set_response_chord_analize(analize_chord_s)