#!/usr/bin/python3

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from libs import CONFIG

# interfaces should be only imported in contoller.py
import interface.audio
import interface.config
import interface.general
import interface.mouse
import interface.vlc

import json
import time



def audioParser(request_json):
    ''' Parse request_json to use requested audio interface function'''
    message = None
    optionalInfo = None
    if 'optionalInfo' in request_json:
        optionalInfo = request_json ['optionalInfo']

    if(request_json['command'] == 'decreaseMasterVolume'):
        message = interface.audio.decreaseMasterVolume()
    elif(request_json['command'] == 'increaseMasterVolume'):
        message = interface.audio.increaseMasterVolume()
    elif(request_json['command'] == 'muteMasterVolume'):
        message = interface.audio.muteMasterVolume()

    return message
    pass

def configParser(request_json):
    ''' Parse request_json to use requested config interface function'''
    message = None
    if(request_json['command'] == 'getConfig'):
        message = interface.config.getConfig(request_json)
    return message

def generalParser(request_json):
    ''' Parse request_json to use requested general interface function'''
    message = None
    optionalInfo = None
    if 'optionalInfo' in request_json:
        optionalInfo = request_json ['optionalInfo']

    if(request_json['command'] == 'getFilesAndFolders'):
        message = interface.general.getFilesAndFolders(optionalInfo['absolutePath'])

    return message

def keyboadParser(request_json):
    ''' Parse request_json to use requested keyboard interface function'''
    message = None
    optionalInfo = None
    if 'optionalInfo' in request_json:
        optionalInfo = request_json ['optionalInfo']
    # TODO: implement keyboard interface
    return message

def mouseParser(request_json):
    ''' Parse request_json to use requested mouse interface function'''
    message = None
    optionalInfo = None
    if 'optionalInfo' in request_json:
        optionalInfo = request_json ['optionalInfo']

    if(request_json['command'] == 'moveMouseX'):
        message = interface.mouse.moveMouseX(optionalInfo['amount'])
    elif(request_json['command'] == 'moveMouseY'):
        message = interface.mouse.moveMouseY(optionalInfo['amount'])
    elif(request_json['command'] == 'leftMouseClick'):
        message =  interface.mouse.leftMouseClick()
    elif(request_json['command'] == 'setMousePosition'):
        message = interface.mouse.setMousePosition(optionalInfo['x'], optionalInfo['y'])

    return message

def vlcParser(request_json):
    ''' Parse request_json to use requested vlc interface function'''
    message = None
    optionalInfo = None
    if 'optionalInfo' in request_json:
        optionalInfo = request_json ['optionalInfo']

    if(request_json['command'] == 'playFile'):
        message = interface.vlc.playFile(optionalInfo['absolutePath'])
    elif(request_json['command'] == 'pauseFile'):
        message = interface.vlc.pauseFile()

    return message


def requestParser(request_json):
    message = None
    if(request_json['interface'] == 'audio'):
        message = audioParser(request_json)
    elif(request_json['interface'] == 'config'):
        message = configParser(request_json)
    elif(request_json['interface'] == 'general'):
        message = generalParser(request_json)
    elif(request_json['interface'] == 'keyboard'):
        message = keyboadParser(request_json)
    elif(request_json['interface'] == 'mouse'):
        message = mouseParser(request_json)
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
