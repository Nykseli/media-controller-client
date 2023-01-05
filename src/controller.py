#!/usr/bin/python3
'''
Main
'''

import os
import signal
import threading
import sys
import json
#import time
from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
#from twisted.python import log
from twisted.internet import reactor
import errors
errors.print_info("Server starting... ")


from libs import CRYPTO_CONFIG, GENERAL_CONFIG, WEBSOCKET_CONFIG
import libs.crypto
import libs.deviceinfo

# Set display envrion so interfaces have the right DISPLAY
if GENERAL_CONFIG and 'display' in GENERAL_CONFIG:
    os.environ['DISPLAY'] = GENERAL_CONFIG['display']

# interfaces should be only imported in contoller.py
import interface
import interface.audio
import interface.browser
import interface.config
import interface.general
import interface.keyboard
import interface.mouse
import interface.vlc as vlc

CRYPTO_SECRET_KEY = None
if CRYPTO_CONFIG:
    CRYPTO_SECRET_KEY = CRYPTO_CONFIG['secretKey']

def audio_parser(request_json):
    ''' Parse request_json to use requested audio interface function'''
    message = None

    if request_json['command'] == 'decreaseMasterVolume':
        message = interface.audio.decrease_master_volume()
    elif request_json['command'] == 'increaseMasterVolume':
        message = interface.audio.increase_master_volume()
    elif request_json['command'] == 'muteMasterVolume':
        message = interface.audio.mute_master_volume()

    return message

def browser_parser(request_json):
    ''' Parse request_json to use the requested browser interface function '''
    message = None

    if request_json['command'] == 'startBrowser':
        message = interface.browser.start_browser()
    elif request_json['command'] == 'stopBrowser':
        message = interface.browser.stop_browser()

    return message

def config_parser(request_json):
    ''' Parse request_json to use requested config interface function'''
    message = None
    if(request_json['command'] == 'getConfig'):
        message = interface.config.get_config()
    return message

def general_parser(request_json):
    ''' Parse request_json to use requested general interface function'''
    message = None
    additional_info = None
    if 'additionalInfo' in request_json:
        additional_info = request_json['additionalInfo']

    if(request_json['command'] == 'getFilesAndFolders'):
        message = interface.general.get_files_and_folders(additional_info['absolutePath'])

    return message

def keyboard_parser(request_json):
    ''' Parse request_json to use requested keyboard interface function'''
    message = None
    additional_info = None
    if 'additionalInfo' in request_json:
        additional_info = request_json['additionalInfo']

    if request_json['command'] == 'inputString':
        message = interface.keyboard.input_string(additional_info['input'])
    elif request_json['command'] == 'pressEnter':
        message = interface.keyboard.press_enter()
    elif request_json['command'] == 'pressTab':
        message = interface.keyboard.press_tab()
    elif request_json['command'] == 'pressBackSpace':
        message = interface.keyboard.press_backspace()
    elif request_json['command'] == 'pressArrowUp':
        message = interface.keyboard.press_arrow_up()
    elif request_json['command'] == 'pressArrowRight':
        message = interface.keyboard.press_arrow_righ()
    elif request_json['command'] == 'pressArrowDown':
        message = interface.keyboard.press_arrow_down()
    elif request_json['command'] == 'pressArrowLeft':
        message = interface.keyboard.press_arrow_left()

    return message

def mouse_parser(request_json):
    ''' Parse request_json to use requested mouse interface function'''
    message = None
    additional_info = None
    if 'additionalInfo' in request_json:
        additional_info = request_json['additionalInfo']

    if request_json['command'] == 'moveMouseX':
        message = interface.mouse.move_mouse_x(additional_info['amount'])
    elif request_json['command'] == 'moveMouseY':
        message = interface.mouse.move_mouse_y(additional_info['amount'])
    elif request_json['command'] == 'leftMouseClick':
        message = interface.mouse.left_mouse_click()
    elif request_json['command'] == 'setMousePosition':
        message = interface.mouse.set_mouse_position(additional_info['x'], additional_info['y'])

    return message

def vlc_parser(request_json):
    ''' Parse request_json to use requested vlc interface function'''
    message = None
    additional_info = None
    if 'additionalInfo' in request_json:
        additional_info = request_json['additionalInfo']

    if request_json['command'] == 'increaseVolume':
        message = interface.vlc.increase_volume()
    elif request_json['command'] == 'decreaseVolume':
        message = interface.vlc.decrease_volume()
    elif request_json['command'] == 'muteVolume':
        message = interface.vlc.mute_volume()
    elif request_json['command'] == 'playFile':
        message = interface.vlc.play_file(additional_info['absolutePath'])
    elif request_json['command'] == 'playFiles':
        message = interface.vlc.play_files(additional_info['absolutePaths'])
    elif request_json['command'] == 'stopMedia':
        message = interface.vlc.stop_media()
    elif request_json['command'] == 'playNextMedia':
        message = interface.vlc.play_next_media()
    elif request_json['command'] == 'playPreviousMedia':
        message = interface.vlc.play_previous_media()
    elif request_json['command'] == 'cycleAudioTrack':
        message = interface.vlc.cycle_audio_track()
    elif request_json['command'] == 'cycleSubtitleTrack':
        message = interface.vlc.cycle_subtitle_track()
    elif request_json['command'] == 'pauseFile':
        message = interface.vlc.pause_file()
    elif request_json['command'] == 'fastForward':
        message = interface.vlc.fast_forward()
    elif request_json['command'] == 'rewind':
        message = interface.vlc.rewind()
    elif request_json['command'] == 'getCurrentlyPlaying':
        message = interface.vlc.get_currently_playing()

    return message


def request_parser(request_json):
    ''' parse requests from websocket '''
    message = None
    if request_json['interface'] == interface.AUDIO_INTERFACE:
        message = audio_parser(request_json)
    elif request_json['interface'] == interface.BROWSER_INTERFACE:
        message = browser_parser(request_json)
    elif request_json['interface'] == interface.CONFIG_INTERFACE:
        message = config_parser(request_json)
    elif request_json['interface'] == interface.GENERAL_INTERFACE:
        message = general_parser(request_json)
    elif request_json['interface'] == interface.KEYBOARD_INTERFACE:
        message = keyboard_parser(request_json)
    elif request_json['interface'] == interface.MOUSE_INTERFACE:
        message = mouse_parser(request_json)
    elif request_json['interface'] == interface.VLC_INTERFACE:
        message = vlc_parser(request_json)

    if message:
        if CRYPTO_SECRET_KEY:
            MyServerProtocol.report_encrypted_message(message)
        else:
            MyServerProtocol.report_message(message)


class MyServerProtocol(WebSocketServerProtocol):
    ''' Class to handle websocet '''
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
            payload = libs.crypto.decrypt_message_cfb(CRYPTO_SECRET_KEY, payload)
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        try:
            request_json = json.loads(payload.decode('utf-8'))
        except Exception as err:
            print(str(err))
            return

        if type(request_json) is dict:
            request_parser(request_json)
        elif type(request_json) is list:
            for command in request_json:
                request_parser(command)

        # echo back message verbatim
        # self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        self.connections.remove(self)
        print("WebSocket connection closed: {0}".format(reason))

    @classmethod
    def report_message(cls, message):
        ''' Report plain text message to all connected clients '''
        payload = json.dumps(message, ensure_ascii=False).encode('utf8')
        for c in set(cls.connections):
            reactor.callFromThread(cls.sendMessage, c, payload)

    @classmethod
    def report_encrypted_message(cls, message):
        ''' Report crypted message to all connected clients '''
        message_string = json.dumps(message, ensure_ascii=False)
        payload = libs.crypto.encrypt_message_cfb(CRYPTO_SECRET_KEY, message_string)
        print(type(payload))
        for c in set(cls.connections):
            reactor.callFromThread(cls.sendMessage, c, payload, True)


class ProgramStopper:
    ''' Listen SIGINT and SIGTERM signals and stop all threads and reactor object when signal recieved '''
    def __init__(self):
        #os.setsid()
        signal.signal(signal.SIGINT, self.set_kill_thread)
        signal.signal(signal.SIGTERM, self.set_kill_thread)

    def set_kill_thread(self, signum, frame):
        # Loop all threads and set kill value to kill
        # Note that this only works if the thread class is implemented
        # in such a way that it stops working when kill is set to True
        for thread in threading.enumerate():
            thread.kill = True

        # Finally stop the reactor object that handles the web socket stuff
        reactor.stop()

if __name__ == '__main__':
    stopper = ProgramStopper()

    if not '--no-vlc' in sys.argv:
        vlc.init()

    WEBSOCKET_PORT = 9000
    if WEBSOCKET_CONFIG and 'port' in WEBSOCKET_CONFIG:
        WEBSOCKET_PORT = WEBSOCKET_CONFIG['port']

    factory = WebSocketServerFactory(u"ws://127.0.0.1:{}".format(WEBSOCKET_PORT))
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    if WEBSOCKET_CONFIG and 'allowedOrigins' in WEBSOCKET_CONFIG:
        factory.setProtocolOptions(allowedOrigins=WEBSOCKET_CONFIG['allowedOrigins'])

    local_ip = libs.deviceinfo.get_local_ip()
    errors.print_info("Server running... Connect to ws://{}:{}".format(local_ip, WEBSOCKET_PORT))

    reactor.listenTCP(WEBSOCKET_PORT, factory)
    reactor.run()
