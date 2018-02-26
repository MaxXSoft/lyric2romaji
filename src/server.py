from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse

html_path = ''
song_file = ''
info_file = ''

class RequestHandler(BaseHTTPRequestHandler):
    # supported MIME-TYPE
    __mime_dic = {
        '.html': 'text/html',
        '.htm': 'text/html',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.info': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.ico': 'image/x-icon',
        '.song': 'audio/mpeg',
    }

    __cur_dir = path.dirname(path.realpath(__file__))

    # GET request
    def do_GET(self):
        server_path = self.__cur_dir + '/' + html_path
        query_path = urlparse(self.path)
        file_path = query_path.path
        if file_path.endswith('/'):
            file_path = server_path + file_path + 'index.html'
        elif file_path.endswith('.mp3'):
            file_path = song_file
        elif file_path.endswith('.json'):
            file_path = info_file
        else:
            file_path = server_path + file_path
        file_ext = path.splitext(file_path)[1]
        mime_type = self.__mime_dic.get(file_ext)
        if mime_type != None:
            try:
                with open(path.realpath(file_path), 'rb') as f:
                    content = f.read()
                    self.send_response_only(200)
                    self.send_header('Content-type', mime_type)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_response_only(404, 'File Not Found: %s' % self.path)
        else:
            self.send_response_only(415)

def getLocalIP(ifname='eth0'):  
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def initServer(port):
    addr = getLocalIP() + ':' + str(port)
    print('starting server at', addr)
    # Server settings
    httpd = HTTPServer(('', port), RequestHandler)
    print('running server...')
    httpd.serve_forever()
