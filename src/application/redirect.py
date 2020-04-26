###
#
#   Full history: see below
#
#   Version: 1.0.0
#   Date: 2020-04-26
#   Author: Yves Vindevogel (vindevoy)
#
#   Original code:
#       https://openvpn.net/vpn-server-resources/how-to-redirect-http-to-https/
#       Adapted to version 3 of Python and slightly modified
#
###

import http.server
import socketserver
import getopt
import sys

PORT = 80
TARGET_URL = 'https://127.0.0.1'


class Redirect(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', TARGET_URL)
        self.end_headers()


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'u:p:', ['url=', 'port='])

    for opt, arg in opts:
        if opt in ['-u', '--url']:
            TARGET_URL = arg
        if opt in ['-p', '--port']:
            PORT = int(arg)

    handler = socketserver.TCPServer(("", PORT), Redirect)
    handler.serve_forever()
