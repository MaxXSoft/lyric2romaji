from urllib.request import urlretrieve
from os import path, mkdir, listdir, remove
import random
import nmapi
import utils.progress as prog

class CacheManager(object):
    def __init__(self, cache_dir='cache'):
        self.__cache_dir = path.dirname(path.realpath(__file__))
        self.__cache_dir += '/' + cache_dir + '/'
        if not path.exists(self.__cache_dir):
            mkdir(self.__cache_dir)
        self.__cache_dict = {}
        self.__prog_bar = prog.ProgressBar()
        self.__loaded_block_count = -1

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

    def cacheSongById(self, song_id, show_progress=True):
        cache_item = self.__cache_dict.get(song_id)
        if cache_item != None:
            return self.__cache_dir + cache_item
        url = nmapi.getSongUrl(song_id)
        cache_item = self.__getCachtUID(song_id)
        save_path = self.__cache_dir + cache_item
        if not path.exists(save_path):
            call_back = None
            if show_progress:
                call_back = self.__showProgress
                print('caching song...')
            urlretrieve(url, save_path, call_back)
        return save_path

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
