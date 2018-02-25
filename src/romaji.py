from urllib import request, parse
import re

class RomajiConverter(object):
    def __init__(self, load_token=True):
        self.__romaji_re = re.compile(r'.?<td class="ruby.*?">(.*?)</td>')
        self.__src_re = re.compile(r'.?<td class="Asian.*?">(.*?)</td>')
        self.__token_re = re.compile(r'<form method="POST".*?><input name="_token".*?value="(.*?)">')
        self.__series_re = re.compile(r'<span class="reading">(.*?)</span>')
        self.__conv_option = 'nothing'
        self.__token = ''
        if load_token: self.getToken()

    def getToken(self):
        # get token from server
        req = request.Request('https://j-talk.com/convert')
        res = request.urlopen(req).read().decode('utf-8')
        self.__token = self.__token_re.findall(res)[0]

    def convert(self, text):
        content = text.strip()
        if self.__token == '': self.getToken()
        # get data from server
        req = request.Request('https://j-talk.com/convert')
        post_data = parse.urlencode({
            '_token': self.__token,
            'content': content,
            'convertOption': self.__conv_option
        })
        res = request.urlopen(req, data=post_data.encode('utf-8'))
        res = res.read().decode('utf-8')
        # start matching
        series = self.__series_re.findall(res)
        # data processing
        result = []
        len_ser = len(series) // 3
        for i in range(len_ser):
            result.append((series[i], series[i + len_ser * 2]))
        return result
    
    def convertFast(self, text):
        # get data from server
        enc_txt = text.strip().encode('unicode_escape').decode('ascii').upper()
        post_data = parse.urlencode({'Text': enc_txt.replace('\\U', '%25u')})
        req = request.Request('http://www.chuanxincao.com/AnimeAPI/LuoMaYinFanYi/')
        res = request.urlopen(req, data=post_data.encode('utf-8'))
        res = res.read().decode('utf-8')
        # start matching
        romaji = self.__romaji_re.findall(res)
        src = self.__src_re.findall(res)
        # data processing
        result = []
        for i in range(len(romaji)):
            result.append((romaji[i].replace('<br>', ','), src[i]))
        return result
