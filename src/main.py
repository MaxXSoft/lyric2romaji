import sys, getopt
import cache, server, nmapi

cm = cache.CacheManager()
server.html_path = '../html/'

help_info = '''
    Lyric->Romaji Usage:
        -h, --help: \t\t\thelp message
        -v, --version: \t\t\tversion info
        -s <name>, --search=<name>: \tsearch song by name
        -i <id>, --id=<id>: \t\tget song by id
        -c, --cache: show cache status
        -e, --clear: clear cached songs
'''
version_info = '''
    Lyric->Romaji Version 0.0.1
    A simple python program that can convert Japanese song lyrics to romaji notation
    2010-2018 MaxXSoft, MaxXing. MIT License
'''

try:
    short_options = 'hvs:i:ce'
    long_options = ['help', 'version', 'search=', 'id=', 'cache', 'clear']
    opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
except getopt.GetoptError:
    print('invalid argument')
    print("use '-h' or '--help' for help")
    exit(1)

if len(opts) == 0:
    print('invalid argument')
    print("use '-h' or '--help' for help")
    exit(1)

if len(sys.argv) == 1:
    print(help_info)
    exit()

mode = 0
argument = ''
for opt, arg in opts:
    if opt in ['-h', '--help']:
        print(help_info)
        exit()
    elif opt in ['-v', '--version']:
        print(version_info)
        exit()
    elif opt in ['-s', '--search']:
        mode = 0
        argument = arg
        break
    elif opt in ['-i', '--id']:
        mode = 1
        argument = arg
        break
    elif opt in ['-c', '--cache']:
        file_num, size_str = cm.getCacheDirSize()
        print('cached', file_num, 'song(s), total size', size_str)
        exit()
    elif opt in ['-e', '--clear']:
        confirm = input('are you sure to clear the cached data? [y/n]: ')
        if confirm.lower() == 'y':
            cm.clearCache()
        exit()

song_id = 0
if mode == 0:
    result = nmapi.searchSongName(argument)
    print('search result: (top 5 only)')
    id_list = []
    for num, i in enumerate(result):
        id_list.append(i['id'])
        song_name = i['name']
        artists = i['artists'][0]['name']
        for j in i['artists'][1:]:
            artists += ', ' + j['name']
        album = i['album']['name']
        print('%d.' % (num + 1), song_name, '-', artists, '-', album)
    id = int(input('please select: ')) - 1
    if not id in range(5):
        print('error: selected invalid id')
        exit(1)
    song_id = id_list[id]
else:
    song_id = int(argument)

print('\ninitializing...\n')
server.song_file, server.info_file = cm.cacheSongById(song_id)
server.initServer(6502, True)
