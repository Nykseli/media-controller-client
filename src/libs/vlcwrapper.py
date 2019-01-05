from subprocess import Popen, check_output, PIPE
from libs import VLC_CONFIG
import os
import signal
import socket
import threading

import time

class VlcWrapper():

    ### Vlc player commands to send over tcp socket ###
    # To see Vlc rc interface commands; open terminal and type vlc -I rc and then longhelp

    # Toggles pause on/off on currently playing media
    PAUSE_FILE = "pause"
    # Play media stream
    PLAY_MEDIA = "play"
    # Add media to playlist
    ADD_TO_PLAYLIST = "add"
    # Clear player playlist
    CLEAR_PLAYLIST = "clear"
    # Set vlc player volume to 0
    MUTE_VOLUME = "volume 0"
    # Loweer audio volume 1 step
    DECREACE_VOLUME = "volup 1"
    # Raise audio volume 1 step
    INCREACE_VOLUME = "voldown 1"
    # Shutdown vlc player
    CLOSE_PLAYER = "shutdown"

    def __init__(self):
        self.vlcProcess = None
        self.HOST = 'localhost'
        self.PORT = 8888
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.initVlcPlayer()

    def initVlcPlayer(self):
        '''Start Vlc process with rc module and connect socket to it'''
        self.killOldVlcProsess()
        self.vlcProcess = Popen(self.getCommandList())
        # Connect to socket with thread so it doesn't block any other functionality
        threading.Thread(target=self.connectSocket).start()

    def killOldVlcProsess(self):
        ''' Kill all vlc procesess '''
        try:
            # subprosess.check_output is syncronous so it blocks until killall is completed
            check_output(['killall', 'vlc'])
        except:
            pass

    def connectSocket(self):
        '''Loops until socket is connected'''
        # connect_ex returns 0 if connection was succesfull
        while self.SOCK.connect_ex((self.HOST, self.PORT)) != 0:
            time.sleep(0.1)

    def getCommandList(self):
        '''
        Get needed commandline arguments to start vlc with rc module.
        If config.json has defined commandlineArguments, append them to arguments
        '''
        argumentList = [
            "vlc",
            "-I",
            "rc",
            "--rc-host=%s:%s" % (self.HOST, self.PORT),
        ]
        if VLC_CONFIG and 'commandlineArguments' in VLC_CONFIG:
            argumentList.extend(VLC_CONFIG['commandlineArguments'])
        return argumentList

    def killCurrent(self):
        os.kill(self.vlcProcess.pid, signal.SIGTERM)
        pass

    def sendVlcCommand(self, cmd):
        '''Prepare a command and send it to VLC'''
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)

    # playFile supports only single file
    def playFile(self, absolutePath):
        '''Clear playlist, add new item to playlist and play it.'''
        self.clearPlaylist()
        self.addToPlaylist(absolutePath)
        self.sendVlcCommand(self.PLAY_MEDIA)

    def pauseFile(self):
        ''' Toggle pause on/off '''
        self.sendVlcCommand(self.PAUSE_FILE)

    def increaseVolume(self):
        ''' Increase Vlc player volume doesn't affect system volume '''
        self.sendVlcCommand(self.INCREACE_VOLUME)

    def decreaseVolume(self):
        ''' Decrease Vlc player volume doesn't affect system volume '''
        self.sendVlcCommand(self.DECREACE_VOLUME)

    def muteVolume(self):
        ''' Mute Vlc player volume doesn't affect system volume '''
        self.sendVlcCommand(self.MUTE_VOLUME)

    def addToPlaylist(self, path):
        command = "{} {}".format(self.ADD_TO_PLAYLIST, path)
        self.sendVlcCommand(command)

    def clearPlaylist(self):
        self.sendVlcCommand(self.CLEAR_PLAYLIST)

    def closePlayer(self):
        ''' Close vlc process and set self.vlcProsess to None '''
        self.vlcProcess = None
        self.sendVlcCommand(self.CLOSE_PLAYER)
