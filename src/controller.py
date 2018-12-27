#!/usr/bin/python3

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from libs.xdotool import XDoTool
from io import BytesIO

import json
import time


# class RequestHandler(BaseHTTPRequestHandler):

#     def handleRequestJson(self, body):
#         try:
#             request_json = json.loads(body.decode('utf-8'))
#         except Exception as err:
#             print(str(err))
#             return
#         print(str(request_json))
#         if(request_json['command'] == 'moveMouseX'):
#             x_tool.moveMouseX(request_json['amount'])

#     def do_POST(self):

#         self.send_response(200)
#         self.send_header("Access-Control-Allow-Origin", "*")
#         self.end_headers()
#         #x_tool.setMousePosition(500, 500)
#         content_length = int(self.headers['Content-Length'])
#         body = self.rfile.read(content_length)
#         self.handleRequestJson(body)
#         print(str(body))
#         response = BytesIO()
#         response.write(b'Received: ')
#         response.write(body)
#         self.wfile.write(response.getvalue())

def requestParser(request_json):
    if(request_json['command'] == 'moveMouseX'):
        x_tool.moveMouseX(request_json['amount'])
    elif(request_json['command'] == 'moveMouseY'):
        x_tool.moveMouseY(request_json['amount'])
    elif(request_json['command'] == 'leftMouseClick'):
        x_tool.leftMouseClick()
    elif(request_json['command'] == 'setMousePosition'):
        x_tool.setMousePosition(request_json['x'], request_json['y'])


class MyServerProtocol(WebSocketServerProtocol):

    connection = None

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.connection = self

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        try:
            request_json = json.loads(payload.decode('utf-8'))
        except Exception as err:
            print(str(err))
            return

        if type(request_json) is dict:
            requestParser(request_json)
        elif type(request_json) is list:
            for command in request_json:
                requestParser(command)

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    @classmethod
    def reportMessage(cls, message):
        cls.callFromThread(cls.sendMessage, self.connection, message)



if __name__ == '__main__':
    x_tool = XDoTool()
    mouse_pos = x_tool.getMousePosition()
    print(mouse_pos)
    x_tool.setMousePosition(100, 200)
    # time.sleep(2)
    # x_tool.moveMouseX(10)
    # time.sleep(2)
    # x_tool.moveMouseY(10)

   # httpd = HTTPServer(('localhost', 8808), RequestHandler)
    #httpd.serve_forever()

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(9000, factory)
    reactor.run()
