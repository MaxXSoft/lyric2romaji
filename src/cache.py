from urllib.request import urlretrieve
from os import path, mkdir, listdir, remove
import random
import nmapi, lrcproc, romaji
import utils.progress as prog
import json

class CacheManager(object):
    def __init__(self, cache_dir='cache'):
        self.__cache_dir = path.dirname(path.realpath(__file__))
        self.__cache_dir += '/' + cache_dir + '/'
        if not path.exists(self.__cache_dir):
            mkdir(self.__cache_dir)
        self.__cache_dict = {}
        self.__prog_bar = prog.ProgressBar()
        self.__loaded_block_count = -1
        self.__lrcp = lrcproc.LyricProcessor()
        self.__rc = romaji.RomajiConverter(load_token=False)

    def __getCachtUID(self, song_id):
        uid = ''
        chrs = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        random.seed(song_id)
        for i in range(32):
            uid += chrs[random.randrange(len(chrs))]
        return uid

    def __showProgress(self, block_count, block_size, file_size):
        self.__prog_bar.total = file_size // block_size
        if self.__loaded_block_count != block_count and self.__prog_bar.percent != 100.0:
            self.__loaded_block_count = block_count
            self.__prog_bar.move()
            self.__prog_bar.log()
    
    def __getLrcInfo(self, song_id):
        lrc, tlrc = self.__lrcp.getNetEaseLyric(song_id)
        lrcl = self.__lrcp.getLyricList(lrc)
        tlrcl = self.__lrcp.getLyricList(tlrc)
        # get plain text lrc
        lrc_str = ''
        start_time = tlrcl[0][0]
        read_flag = False
        for i, j in lrcl:
            if not read_flag and i == start_time:
                read_flag = True
            if read_flag:
                lrc_str += j + '\n'
        # get romaji lyric list
        romaji_pair = self.__rc.convertFast(lrc_str)
        romaji_lrc = []
        tmp_txt = ''
        cur_pos = 0
        for r, t in romaji_pair:
            if '\\N' in t:
                romaji_lrc.append((tlrcl[cur_pos][0], tmp_txt.strip()))
                tmp_txt = ''
                cur_pos += 1
            elif r != '':
                tmp_txt += r + ' '
        if tmp_txt != '':
            romaji_lrc.append((tlrcl[cur_pos][0], tmp_txt.strip()))
        # merge lyric lists
        merged = self.__lrcp.mergeLyricList(lrcl, tlrcl, romaji_lrc)
        return merged

    def __getSongInfo(self, song_id):
        info = {}
        # save song details
        song_detail = nmapi.getSongDetail(song_id)
        info['name'] = song_detail['name']
        # save artists info
        artists = []
        for i in song_detail['artists']:
            artists.append(i['name'])
        info['artists'] = artists
        # save album info
        info['album'] = {
            'name': song_detail['album']['name'],
            'pic': song_detail['album']['picUrl']
        }
        # get lrc info
        info['lrc'] = self.__getLrcInfo(song_id)
        # return string in JSON format
        return info

    def cacheSongById(self, song_id, show_progress=True):
        cache_item = self.__cache_dict.get(song_id)
        # already cached
        if cache_item != None:
            save_path = self.__cache_dir + cache_item
            return save_path + '.song', save_path + '.info'
        cache_item = self.__getCachtUID(song_id)
        save_path = self.__cache_dir + cache_item
        if not path.exists(save_path + '.song'):
            # save info cache
            if show_progress:
                print('caching song info...')
            info = self.__getSongInfo(song_id)
            json.dump(info, open(save_path + '.info', 'w'))
            # save song cache
            call_back = None
            if show_progress:
                call_back = self.__showProgress
                print('caching song...')
            url = nmapi.getSongUrl(song_id)
            urlretrieve(url, save_path + '.song', call_back)
        return save_path + '.song', save_path + '.info'

    def getCacheDirSize(self):
        size = 0
        for f in listdir(self.__cache_dir):
            cur_file = path.join(self.__cache_dir, f)
            if path.isfile(cur_file):
                size += path.getsize(cur_file)
        size_str = ''
        if size >= 1024 ** 3 * 0.9:
            size_str = '%.2f GB' % (size / 1024 ** 3)
        else:
            size_str = '%.2f MB' % (size / 1024 ** 2)
        return size, size_str

    def clearCache(self):
        for f in listdir(self.__cache_dir):
            cur_file = path.join(self.__cache_dir, f)
            if path.isfile(cur_file):
                remove(cur_file)

if __name__ == '__main__':
    cm = CacheManager()
    print(cm.cacheSongById(26124993))
