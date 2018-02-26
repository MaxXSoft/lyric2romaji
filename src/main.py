import cache, server

cm = cache.CacheManager()
server.html_path = '../html/'
server.song_file, server.info_file = cm.cacheSongById(26124993)
server.initServer(6502)

