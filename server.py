import SocketServer

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


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "Got a request of: %s\n" % self.data
        self.request.sendall("OK")


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
