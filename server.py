import SocketServer
import os

# Copyright 2015 Tianyi Wu, Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright (AT) 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

HTML_PATH = 'www'

MIME_TYPE = {
    "CSS": "text/css",
    "HTML": "text/html"
}

HTTP_CODE = {
    200: ('OK', 'Request fulfilled, document follows'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    400: ('Bad Request', 'Bad request syntax or unsupported method'),
    404: ('Not Found', 'Nothing matches the given URI'),
    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented', 'Server does not support this operation'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request')
}


ERROR_TEMPLATE = """\
<head>
<title>{code} {msg}</title>
</head>
<body>
<h1>{code} {msg}</h1>
<p>{reason}.
</body>
"""


class HTTPError(Exception):

    def __init__(self, status_code=500):
        self.status_info = HTTP_CODE[status_code]
        self.status_code = status_code
        self.status_msg = self.status_info[0]
        self.status_reason = self.status_info[1]

    @property
    def html_content(self):
        return ERROR_TEMPLATE.format(code=self.status_code,
                                     msg=self.status_msg,
                                     reason=self.status_reason)


class MyWebServer(SocketServer.BaseRequestHandler):

    SUPPORTED_HTTP_VERSION = ('HTTP/1.0', 'HTTP/1.1')
    SUPPORTED_METHODS = ("GET")

    def get(self, path):
        root_path = os.path.abspath(HTML_PATH)

        file_path = root_path + path
        absolute_path = os.path.abspath(file_path)

        if not absolute_path.startswith(root_path):
            raise HTTPError(404)

        if not os.path.exists(absolute_path):
            raise HTTPError(404)

        if os.path.isdir(absolute_path):
            if not file_path.endswith('/'):
                self.redirect(path + '/')

            absolute_path = os.path.join(absolute_path, 'index.html')

        mime_type = MIME_TYPE.get(
            absolute_path.split('.')[-1].upper(), MIME_TYPE['HTML'])
        with open(absolute_path) as fp:
            self.send_response(200, mime_type, fp.read())

    def redirect(self, path):
        response = "HTTP/1.1 %d %s\r\n" % (301, HTTP_CODE[301][0])
        response += "Location: %s\r\n\r\n" % path

        self.request.sendall(response)

    def send_response(self, code, mime_type, content=''):
        response = "HTTP/1.1 %d %s \r\n" % (code, HTTP_CODE[code][0])
        response += "Content-Length: %d \r\n" % len(content)
        response += "Content-Type: %s \r\n" % mime_type
        response += "Connection: close \r\n\r\n"
        response += content
        response += "\r\n"

        self.request.sendall(response)

    def send_error(self, e):
        self.send_response(e.status_code, MIME_TYPE['HTML'], e.html_content)

    def http_request(self, req):
        req_args = req.splitlines()[0].split()

        if len(req_args) != 3:
            raise HTTPError(400)

        req_method, path, http_version = req_args

        if http_version.strip() not in self.SUPPORTED_HTTP_VERSION:
            raise HTTPError(505)

        if req_method not in self.SUPPORTED_METHODS:
            raise HTTPError(405)

        method = getattr(self, req_method.lower())
        method(path)

    def handle(self):
        self.data = self.request.recv(1024).strip()

        try:
            self.http_request(self.data)
        except HTTPError as e:
            self.send_error(e)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
