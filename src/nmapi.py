# reference: https://github.com/darknessomi/musicbox/blob/master/NEMbox/api.py

from urllib import request, parse
import json
import random, os, base64, binascii
from Crypto.Cipher import AES   # PyCrypto required

def encryptAES(text, sec_key):
    pad = 16 - len(text) % 16
    text = text + chr(pad) * pad
    encryptor = AES.new(sec_key, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext

def encryptRSA(text, pub_key, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pub_key, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)

def createSecretKey(size):
    return binascii.hexlify(os.urandom(size))[:16]

# get encrypted post data
def getEncryptedRequest(text):
    modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
               'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
               '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
               '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
               '3ece0462db0a22b8e7')
    nonce = '0CoJUm6Qyw8W8jud'
    pub_key = '010001'
    text = json.dumps(text)
    sec_key = createSecretKey(16)
    enc_text = encryptAES(encryptAES(text, nonce), sec_key)
    enc_sec_key = encryptRSA(sec_key, pub_key, modulus)
    data = {'params': enc_text, 'encSecKey': enc_sec_key}
    return parse.urlencode(data)

def getMp3Info(song_id, quality='l'):
    # get song detail
    detail_url = 'http://music.163.com/api/song/detail/?id={}&ids=[{}]'
    req = request.Request(detail_url.format(song_id, song_id))
    req.add_header('User-Agent', '')
    res = request.urlopen(req).read().decode('utf-8')
    data = json.loads(res)
    # get mp3 info by quality
    quality_id = quality + 'Music'
    return data['songs'][0][quality_id]

def getSongUrl(song_id, quality='l'):
    mp3_info = getMp3Info(song_id, quality)
    if mp3_info == None:
        # no matching quality
        return ''
    url_req = {'ids': [song_id], 'br': mp3_info['bitrate'], 'csrf_token': ''}
    enc_req = getEncryptedRequest(url_req)
    # post request
    post_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
    req = request.Request(post_url)
    req.add_header('User-Agent', '')
    res = request.urlopen(req, data=enc_req.encode('utf-8'))
    # parse the data
    url_data = json.loads(res.read().decode('utf-8'))
    return url_data['data'][0]['url']

def searchSongName(name, limit=5):
    post_data = parse.urlencode({'s': name, 'type': 1, 'limit': limit})
    req = request.Request('http://music.163.com/api/search/get')
    res = request.urlopen(req, data=post_data.encode('utf-8'))
    data = json.loads(res.read().decode('utf-8'))
    return data['result']['songs']
