#!/usr/bin/python3

import os
import errors
import signal
import threading
errors.printInfo("Server starting... ")

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from libs import CRYPTO_CONFIG, GENERAL_CONFIG, WEBSOCKET_CONFIG
import libs.crypto
import libs.deviceinfo

# Set display envrion so interfaces have the right DISPLAY
if GENERAL_CONFIG and 'display' in GENERAL_CONFIG:
    os.environ['DISPLAY'] = GENERAL_CONFIG['display']

# interfaces should be only imported in contoller.py
import interface
import interface.audio
import interface.config
import interface.general
import interface.keyboard
import interface.mouse
import interface.vlc

import json
import time


CRYPTO_SECRET_KEY = None
if CRYPTO_CONFIG:
    CRYPTO_SECRET_KEY = CRYPTO_CONFIG['secretKey']

def audioParser(request_json):
    ''' Parse request_json to use requested audio interface function'''
    message = None
    additionalInfo = None
    if 'additionalInfo' in request_json:
        additionalInfo = request_json ['additionalInfo']

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
    additionalInfo = None
    if 'additionalInfo' in request_json:
        additionalInfo = request_json ['additionalInfo']

    if(request_json['command'] == 'getFilesAndFolders'):
        message = interface.general.getFilesAndFolders(additionalInfo['absolutePath'])

    return message

def keyboardParser(request_json):
    ''' Parse request_json to use requested keyboard interface function'''
    message = None
    additionalInfo = None
    if 'additionalInfo' in request_json:
        additionalInfo = request_json ['additionalInfo']

    if(request_json['command'] == 'inputString'):
        message = interface.keyboard.inputString(additionalInfo['input'])
    elif(request_json['command'] == 'pressEnter'):
        message = interface.keyboard.pressEnter()
    elif(request_json['command'] == 'pressTab'):
        message = interface.keyboard.pressTab()
    elif(request_json['command'] == 'pressBackSpace'):
        message = interface.keyboard.pressBackSpace()
    elif(request_json['command'] == 'pressArrowUp'):
        message = interface.keyboard.pressArrowUp()
    elif(request_json['command'] == 'pressArrowRight'):
        message = interface.keyboard.pressArrowRight()
    elif(request_json['command'] == 'pressArrowDown'):
        message = interface.keyboard.pressArrowDown()
    elif(request_json['command'] == 'pressArrowLeft'):
        message = interface.keyboard.pressArrowLeft()

    return message

def mouseParser(request_json):
    ''' Parse request_json to use requested mouse interface function'''
    message = None
    additionalInfo = None
    if 'additionalInfo' in request_json:
        additionalInfo = request_json ['additionalInfo']

    if(request_json['command'] == 'moveMouseX'):
        message = interface.mouse.moveMouseX(additionalInfo['amount'])
    elif(request_json['command'] == 'moveMouseY'):
        message = interface.mouse.moveMouseY(additionalInfo['amount'])
    elif(request_json['command'] == 'leftMouseClick'):
        message =  interface.mouse.leftMouseClick()
    elif(request_json['command'] == 'setMousePosition'):
        message = interface.mouse.setMousePosition(additionalInfo['x'], additionalInfo['y'])

    return message

def vlcParser(request_json):
    ''' Parse request_json to use requested vlc interface function'''
    message = None
    additionalInfo = None
    if 'additionalInfo' in request_json:
        additionalInfo = request_json ['additionalInfo']

    if(request_json['command'] == 'increaseVolume'):
        message = interface.vlc.increaseVolume()
    elif(request_json['command'] == 'decreaseVolume'):
        message = interface.vlc.decreaseVolume()
    elif(request_json['command'] == 'muteVolume'):
        message = interface.vlc.muteVolume()
    elif(request_json['command'] == 'playFile'):
        message = interface.vlc.playFile(additionalInfo['absolutePath'])
    elif(request_json['command'] == 'playFiles'):
        message = interface.vlc.playFiles(additionalInfo['absolutePaths'])
    elif(request_json['command'] == 'playNextMedia'):
        message = interface.vlc.playNextMedia()
    elif(request_json['command'] == 'playPreviousMedia'):
        message = interface.vlc.playPreviousMedia()
    elif(request_json['command'] == 'cycleAudioTrack'):
        message = interface.vlc.cycleAudioTrack()
    elif(request_json['command'] == 'cycleSubtitleTrack'):
        message = interface.vlc.cycleSubtitleTrack()
    elif(request_json['command'] == 'pauseFile'):
        message = interface.vlc.pauseFile()
    elif(request_json['command'] == 'fastForward'):
        message = interface.vlc.fastForward()
    elif(request_json['command'] == 'rewind'):
        message = interface.vlc.rewind()
    elif(request_json['command'] == 'getCurrentlyPlaying'):
        message = interface.vlc.getCurrentlyPlaying()

    return message


def requestParser(request_json):
    message = None
    if(request_json['interface'] == interface.AUDIO_INTERFACE):
        message = audioParser(request_json)
    elif(request_json['interface'] == interface.CONFIG_INTERFACE):
        message = configParser(request_json)
    elif(request_json['interface'] == interface.GENERAL_INTERFACE):
        message = generalParser(request_json)
    elif(request_json['interface'] == interface.KEYBOARD_INTERFACE):
        message = keyboardParser(request_json)
    elif(request_json['interface'] == interface.MOUSE_INTERFACE):
        message = mouseParser(request_json)
    elif(request_json['interface'] == interface.VLC_INTERFACE):
        message = vlcParser(request_json)

    if message:
        if CRYPTO_SECRET_KEY:
            MyServerProtocol.reportCryptedMessage(message)
        else:
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
            # Byte data is interpeted as crypted messsage
            payload = libs.crypto.decryptMessageCFB(CRYPTO_SECRET_KEY, payload)
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
        # self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        self.connections.remove(self)
        print("WebSocket connection closed: {0}".format(reason))

    @classmethod
    def reportMessage(cls, message):
        ''' Report plain text message to all connected clients '''
        payload = json.dumps(message, ensure_ascii = False).encode('utf8')
        for c in set(cls.connections):
            reactor.callFromThread(cls.sendMessage, c, payload)

    @classmethod
    def reportCryptedMessage(cls, message):
        ''' Report crypted message to all connected clients '''
        messageStr = json.dumps(message, ensure_ascii = False)
        payload = libs.crypto.cryptMessageCFB(CRYPTO_SECRET_KEY, messageStr)
        print(type(payload))
        for c in set(cls.connections):
            reactor.callFromThread(cls.sendMessage, c, payload, True)


class ProgramStopper:
    ''' Listen SIGINT and SIGTERM signals and stop all threads and reactor object when signal recieved '''
    def __init__(self):
        #os.setsid()
        signal.signal(signal.SIGINT, self.setKillThread)
        signal.signal(signal.SIGTERM, self.setKillThread)

    def setKillThread(self, signum, frame):
        # Loop all threads and set kill value to kill
        # Note that this only works if the thread class is implemented
        # in such a way that it stops working when kill is set to True
        for thread in threading.enumerate():
            thread.kill = True

        # Finally stop the reactor object that handles the web socket stuff
        reactor.stop()

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    #log.startLogging(sys.stdout)

    stopper = ProgramStopper()

    WEBSOCKET_PORT = 9000
    if WEBSOCKET_CONFIG and 'port' in WEBSOCKET_CONFIG:
        WEBSOCKET_PORT = WEBSOCKET_CONFIG['port']

    factory = WebSocketServerFactory(u"ws://127.0.0.1:{}".format(WEBSOCKET_PORT))
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    if WEBSOCKET_CONFIG and 'allowedOrigins' in WEBSOCKET_CONFIG:
        factory.setProtocolOptions(allowedOrigins=WEBSOCKET_CONFIG['allowedOrigins'])

    localIp = libs.deviceinfo.getLocalIp()
    errors.printInfo("Server running... Connect to ws://{}:{}".format(localIp, WEBSOCKET_PORT))

    reactor.listenTCP(WEBSOCKET_PORT, factory)
    reactor.run()
