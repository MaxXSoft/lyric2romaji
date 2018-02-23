from urllib import request
import re
import json

lrc_re = re.compile(r'\[(.*?)\]+(.*)')

def getNeteaseLyric(song_id):
    lrc_url = 'http://music.163.com/api/song/lyric?id={}&lv=1&tv=-1'
    req = request.Request(lrc_url.format(song_id))
    res = request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    lrc = data['lrc']['lyric']
    tlrc = data['tlyric']['lyric']
    return lrc, tlrc

def getLyricList(lrc, trans_lrc=''):
    lrc_data = lrc_re.findall(lrc)
    tlrc_data = lrc_re.findall(trans_lrc)
    return lrc_data

print(getLyricList('[1][2]a'))
