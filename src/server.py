from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse

html_path = '../html/'

class TinyServer(BaseHTTPRequestHandler):
    # supported MIME-TYPE
    __mime_dic = {
        '.html': 'text/html',
        '.htm': 'text/html',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.txt': 'text/plain',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.gif': 'image/gif',
        '.ico': 'image/x-icon',
        '.mp3': 'audio/mpeg',
    }

    __cur_dir = path.dirname(path.realpath(__file__)) + '/' + html_path

    # GET request
    def do_GET(self):
        query_path = urlparse(self.path)
        file_path = query_path.path
        if file_path.endswith('/'):
            file_path += 'index.html'
        file_ext = path.splitext(file_path)[1]
        mime_type = self.__mime_dic.get(file_ext)
        if mime_type != None:
            try:
                print(self.__cur_dir)
                with open(path.realpath(self.__cur_dir + file_path), 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mime_type)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)
        else:
            self.send_error(415)

def initServer(port):
    print('starting server, port', port)
    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, TinyServer)
    print('running server...')
    httpd.serve_forever()

if __name__ == '__main__':
    initServer(6502)
