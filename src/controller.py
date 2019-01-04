#!/usr/bin/python3

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from libs.xdotool import XDoTool
from libs.filemanager import FileManager
from libs.audiomanager import AudioManager
from libs.vlcwrapper import VlcWrapper
from libs import CONFIG
from io import BytesIO

import json
import time


def returnConfig(request_json):
    config = {}
    config['config'] = {}
    configType = request_json['configType']
    if(configType == "vlc"):
        config['config']['vlc'] = CONFIG['vlc']

    elif(configType == 'all'):
        config['config'] = CONFIG
    else:
        config['config'] = CONFIG

    return config

def configParser(request_json):
    message = None
    if(request_json['command'] == 'getConfig'):
        message = returnConfig(request_json)
    return message

def generalParser(request_json):
    message = None
    optionalInfo = None
    if 'optionalInfo' in request_json:
        optionalInfo = request_json ['optionalInfo']

    if(request_json['command'] == 'moveMouseX'):
        message = x_tool.moveMouseX(optionalInfo['amount'])
    elif(request_json['command'] == 'moveMouseY'):
        message = x_tool.moveMouseY(optionalInfo['amount'])
    elif(request_json['command'] == 'leftMouseClick'):
        message =  x_tool.leftMouseClick()
    elif(request_json['command'] == 'setMousePosition'):
        message = x_tool.setMousePosition(optionalInfo['x'], optionalInfo['y'])
    elif(request_json['command'] == 'getFilesAndFolders'):
        message = fileManager.getFilesAndFolders(optionalInfo['absolutePath'])
    elif(request_json['command'] == 'increaseMasterVolume'):
        message = audioManager.increaseMasterVolume()
    elif(request_json['command'] == 'decreaseMasterVolume'):
        message = audioManager.decreaseMasterVolume()
    elif(request_json['command'] == 'muteMasterVolume'):
        message = audioManager.muteMasterVolume()
    return message


def vlcParser(request_json):
    message = None
    optionalInfo = None
    if 'optionalInfo' in request_json:
        optionalInfo = request_json ['optionalInfo']

    if(request_json['command'] == 'playFile'):
        message = vlcWrapper.playFile(optionalInfo['absolutePath'])
    elif(request_json['command'] == 'pauseFile'):
        message = vlcWrapper.pauseFile()
    return message


def requestParser(request_json):
    message = None
    if(request_json['interface'] == 'config'):
        message = configParser(request_json)
    elif(request_json['interface'] == 'general'):
        message = generalParser(request_json)
    elif(request_json['interface'] == 'vlc'):
        message = vlcParser(request_json)

    if message:
        MyServerProtocol.reportMessage(message)


class MyServerProtocol(WebSocketServerProtocol):

    connections = []

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.connections.append(self)

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
        self.connections.remove(self)
        print("WebSocket connection closed: {0}".format(reason))

    @classmethod
    def reportMessage(cls, message):
        payload = json.dumps(message, ensure_ascii = False).encode('utf8')
        for c in set(cls.connections):
            reactor.callFromThread(cls.sendMessage, c, payload)



if __name__ == '__main__':

    x_tool = XDoTool()
    fileManager = FileManager()
    audioManager = AudioManager()
    vlcWrapper = VlcWrapper()

    print("loaded config: " + json.dumps(CONFIG['vlc']))

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
