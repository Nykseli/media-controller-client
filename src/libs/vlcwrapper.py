from subprocess import Popen, check_output, PIPE
from libs import VLC_CONFIG
import os
import errno
import errors
#import fcntl
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
    # Enqueue media to playlist
    ENQUEUE_TO_PLAYLIST = "enqueue"
    # Play next item in medialist
    PLAY_NEXT_MEDIA = "next"
    # Play previous item in medialist
    PLAY_PREVIOUS_MEDIA = "prev"
    # Clear player playlist
    CLEAR_PLAYLIST = "clear"
    # Set vlc player volume to 0
    MUTE_VOLUME = "volume 0"
    # Loweer audio volume 1 step
    DECREACE_VOLUME = "voldown 1"
    # Raise audio volume 1 step
    INCREACE_VOLUME = "volup 1"
    # Shutdown vlc player
    CLOSE_PLAYER = "shutdown"
    # Get title of currently playing media
    CURRENTLY_PLAYING = "get_title"

    ## List of hotkeys can be found https://wiki.videolan.org/Hotkeys_table
    # Toggle mute on/off
    HOTKEY_VOLUME_MUTE = "hotkey key-vol-mute"
    # Increase Volume by 5%
    HOTKEY_VOLUME_INCREASE = "hotkey key-vol-up"
    # Increase Volume by 5%
    HOTKEY_VOLUME_DECREASE = "hotkey key-vol-down"
    # Fastforward 10 secods
    HOTKEY_FAST_FORWARD = "hotkey key-jump+short"
    # Rewind 10 secods
    HOTKEY_FAST_REWIND = "hotkey key-jump-short"
    # Cycle audio track
    HOTKEY_CYCLE_AUDIO = "hotkey key-audio-track"
    # Cycle subltitle track
    HOTKEY_CYCLE_SUBTITLE = "hotkey key-subtitle-track"

    ### Default socket variables ###
    # Default socket host. TODO: make this configurable in config.json
    SOCKET_HOST = 'localhost'
    # Default socket port. TODO: make this configurable in config.json
    SOCKET_PORT = 8888
    # Defines how long recv waits data to show in buffer before timing out
    SOCKET_TIMEOUT = 0.1
    # Buffer reader bytes amount.
    # This defines maximum amount of bytes that the socket can read from buffer
    BUFFER_BYTE_AMOUNT = 4096
    # Encoding that is used to decode data from socket buffer
    BUFFER_ENCODING = 'utf-8'



    def __init__(self):
        self.vlcProcess = None
        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.initVlcPlayer()

    def initVlcPlayer(self):
        '''Start Vlc process with rc module and connect socket to it'''
        self.__killOldVlcProsess()
        self.vlcProcess = Popen(self.__getCommandList(), env=os.environ.copy(), stdout=PIPE)
        # Excecute __initSocketConnection on thread so it doesn't block
        # other functionality if there is a problem with connecting
        threading.Thread(target=self.__initSocketConnection).start()

    def __killOldVlcProsess(self):
        ''' Kill all vlc procesess '''
        try:
            # subprosess.check_output is syncronous so it blocks until killall is completed
            check_output(['killall', 'vlc'])
        except:
            pass

    def __initSocketConnection(self):
        '''Init rc module socket connection'''
        # Loop until socket is connected
        # connect_ex returns 0 if connection was succesful
        while self.SOCK.connect_ex((self.SOCKET_HOST, self.SOCKET_PORT)) != 0:
            time.sleep(0.1)

        errors.printInfo("Vlc player started!")

        # Set socket time out so it waits a while to make sure data is written to buffer
        # This also prevents reading from buffer from blocking
        self.SOCK.settimeout(self.SOCKET_TIMEOUT)
        # When rc module starts, it writes data to socket buffer that we don't
        # want to read later
        self.__emptyReaderBuffer()

    def __getCommandList(self):
        '''
        Get needed commandline arguments to start vlc with rc module.
        If config.json has defined commandlineArguments, append them to arguments
        '''
        argumentList = [
            "vlc",
            "-I",
            "rc",
            "--rc-host={}:{}".format(self.SOCKET_HOST, self.SOCKET_PORT),
        ]
        if VLC_CONFIG and 'commandlineArguments' in VLC_CONFIG:
            argumentList.extend(VLC_CONFIG['commandlineArguments'])
        return argumentList

    def killCurrent(self):
        os.kill(self.vlcProcess.pid, signal.SIGTERM)
        pass

    def sendVlcCommand(self, cmd, emptyBuffer=True):
        '''
        Prepare a command and send it to VLC and empty socket buffer by default.
        Set seconda argument emptyBuffer if you need the data from
        socket buffer e.g. currently playing title
        '''
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)

        if emptyBuffer:
            self.__emptyReaderBuffer()

    # playFile supports only single file
    def playFile(self, absolutePath):
        '''Clear playlist, add new item to playlist and play it.'''
        self.clearPlaylist()
        self.addToPlaylist(absolutePath)
        self.sendVlcCommand(self.PLAY_MEDIA)

    def playFiles(self, paths):
        ''' Clear playlist, add new items from path array to playlist and play them. '''
        self.clearPlaylist()
        for file in paths:
            #print(file)
            self.enqueueToPlaylist(file)
        self.sendVlcCommand(self.PLAY_MEDIA)

    def pauseFile(self):
        ''' Toggle pause on/off '''
        self.sendVlcCommand(self.PAUSE_FILE)

    def fastForward(self):
        ''' Fast forward 10 secods'''
        self.sendVlcCommand(self.HOTKEY_FAST_FORWARD)

    def rewind(self):
        ''' Rewind 10 secods'''
        self.sendVlcCommand(self.HOTKEY_FAST_REWIND)

    def increaseVolume(self):
        ''' Increase Vlc player volume doesn't affect system volume '''
        self.sendVlcCommand(self.HOTKEY_VOLUME_INCREASE)

    def decreaseVolume(self):
        ''' Decrease Vlc player volume doesn't affect system volume '''
        self.sendVlcCommand(self.HOTKEY_VOLUME_DECREASE)

    def muteVolume(self):
        ''' Mute Vlc player volume doesn't affect system volume '''
        self.sendVlcCommand(self.HOTKEY_VOLUME_MUTE)

    def addToPlaylist(self, path):
        '''Add item to playlist path should be absolute path'''
        command = "{} {}".format(self.ADD_TO_PLAYLIST, path)
        self.sendVlcCommand(command)

    def enqueueToPlaylist(self, path):
        '''Enqueue item to playlist path should be absolute path'''
        command = "{} {}".format(self.ENQUEUE_TO_PLAYLIST, path)
        self.sendVlcCommand(command)

    def clearPlaylist(self):
        ''' Clear all the medias from current vlc medialist '''
        self.sendVlcCommand(self.CLEAR_PLAYLIST)

    def cycleAudioTrack(self):
        ''' Cycle through audio tracks '''
        self.sendVlcCommand(self.HOTKEY_CYCLE_AUDIO)

    def cycleSubtitleTrack(self):
        ''' Cycle through subtitle tracks '''
        self.sendVlcCommand(self.HOTKEY_CYCLE_SUBTITLE)

    def playPreviousMedia(self):
        ''' Play previous media in medialist '''
        self.sendVlcCommand(self.PLAY_PREVIOUS_MEDIA)

    def playNextMedia(self):
        ''' Play next media in medialist '''
        self.sendVlcCommand(self.PLAY_NEXT_MEDIA)

    def closePlayer(self):
        ''' Close vlc process and set self.vlcProsess to None '''
        self.vlcProcess = None
        self.sendVlcCommand(self.CLOSE_PLAYER)

    def getCurrentlyPlaying(self):
        '''Get title of currently playing media'''
        self.sendVlcCommand("get_title", False)
        return self.__formatedSocketData()

    def __formatedSocketData(self) -> str:
        '''
        Get data from socket buffer, decode it and remove four last useless bytes
        that vlc rc module always writes to socket buffer
        '''
        bufferData = self.__readDataFromSocket()
        bufferString = bufferData.decode(self.BUFFER_ENCODING)
        # remove "\t\n> " string from end
        return bufferString[:-4]

    def __emptyReaderBuffer(self):
        ''' Read data from buffer until there is data. This makes sure that buffer is empty '''
        while True:
            data = self.__readDataFromSocket()
            if not data:
                time.sleep(0.1)
            else:
                # Data found
                break

    def __readDataFromSocket(self) -> bytes:
        """ Try to read data from socket. Return empty bytes if no data currently in the buffer. """
        try:
            return self.SOCK.recv(self.BUFFER_BYTE_AMOUNT)
        except Exception as err:
            # No data
            pass
        return b''
