import cache, server

cm = cache.CacheManager()
server.html_path = '../html/'
server.initServer(6502)

