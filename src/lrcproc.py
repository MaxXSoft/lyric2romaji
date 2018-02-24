from urllib import request
import re, json

class LyricProcessor(object):
    def __init__(self):
        self.__lrc_re = re.compile(r'\[(.*)\](.*)')

    def getNetEaseLyric(self, song_id):
        lrc_url = 'http://music.163.com/api/song/lyric?id={}&lv=1&tv=-1'
        # get lyric data from Netease Music
        req = request.Request(lrc_url.format(song_id))
        res = request.urlopen(req).read().decode('utf-8')
        data = json.loads(res)
        # parse JSON
        lrc = data['lrc']['lyric']
        tlrc = data['tlyric']['lyric']
        return lrc, tlrc

    def getLyricList(self, lrc):
        lrc_data = self.__lrc_re.findall(lrc)
        lrc_list = []
        for i in lrc_data:
            # convert time code from text to integer in order to sort
            time_code = i[0].replace(':', '').replace('.', '').split('][')
            if i[1] != '':
                for j in time_code:
                    lrc_list.append((int(j), i[1]))
        return sorted(lrc_list, key=lambda x: x[0])

    def mergeLyricList(self, *lrc_lists):
        merged = {}
        for l in lrc_lists:
            for i in l:
                item = merged.setdefault(i[0], [])
                item.append(i[1])
        return merged

    def getTimeCodeText(self, time_code):
        text = str(time_code // 10000).zfill(2) + ':'
        text += str(time_code // 100 % 100).zfill(2) + '.'
        text += str(time_code % 100).zfill(2)
        return text
