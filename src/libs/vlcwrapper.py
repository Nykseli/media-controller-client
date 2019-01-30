'''
vlcwrapper contains a class that wraps vlc controller
'''

from subprocess import Popen, check_output, PIPE
import os
#mport errno
#import fcntl
import signal
import socket
import threading
import time

import errors

from libs import VLC_CONFIG

class VlcWrapper():
    ''' Class used to controll vlc player via tcp socket'''
    ### Vlc player commands to send over tcp socket ###
    # To see Vlc rc interface commands; open terminal and type vlc -I rc and then longhelp

    # Toggles pause on/off on currently playing media
    PAUSE_FILE = "pause"
    # Play media stream
    PLAY_MEDIA = "play"
    # Stop media stream
    STOP_MEDIA = "stop"
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
        self.vlc_process = None
        self.vlc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_vlc_player()

    def init_vlc_player(self):
        '''Start Vlc process with rc module and connect socket to it'''
        self.__kill_old_vlc_processes()
        self.vlc_process = Popen(self.__get_commands_list(), env=os.environ.copy(), stdout=PIPE)
        # Excecute __init_socket_connection on thread so it doesn't block
        # other functionality if there is a problem with connecting
        threading.Thread(target=self.__init_socket_connection).start()

    def __kill_old_vlc_processes(self):
        ''' Kill all vlc procesess '''
        try:
            # subprosess.check_output is syncronous so it blocks until killall is completed
            check_output(['killall', 'vlc'])
        except:
            pass

    def __init_socket_connection(self):
        '''Init rc module socket connection'''
        # Loop until socket is connected
        # connect_ex returns 0 if connection was succesful
        while self.vlc_socket.connect_ex((self.SOCKET_HOST, self.SOCKET_PORT)) != 0:
            time.sleep(0.1)

        errors.print_info("Vlc player started!")

        # Set socket time out so it waits a while to make sure data is written to buffer
        # This also prevents reading from buffer from blocking
        self.vlc_socket.settimeout(self.SOCKET_TIMEOUT)
        # When rc module starts, it writes data to socket buffer that we don't
        # want to read later
        self.__empty_reader_buffer()

    def __get_commands_list(self):
        '''
        Get needed commandline arguments to start vlc with rc module.
        If config.json has defined commandlineArguments, append them to arguments
        '''
        argument_list = [
            "vlc",
            "-I",
            "rc",
            "--rc-host={}:{}".format(self.SOCKET_HOST, self.SOCKET_PORT),
        ]
        if VLC_CONFIG and 'commandlineArguments' in VLC_CONFIG:
            argument_list.extend(VLC_CONFIG['commandlineArguments'])
        return argument_list

    def kill_current(self):
        ''' kill current vlc process '''
        os.kill(self.vlc_process.pid, signal.SIGTERM)


    def send_vlc_command(self, cmd, empty_buffer=True):
        '''
        Prepare a command and send it to VLC and empty socket buffer by default.
        Set seconda argument empty_buffer if you need the data from
        socket buffer e.g. currently playing title
        '''
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.vlc_socket.sendall(cmd)

        if empty_buffer:
            self.__empty_reader_buffer()

    # play_file supports only single file
    def play_file(self, absolute_path):
        '''Clear playlist, add new item to playlist and play it.'''
        self.clear_playlist()
        self.add_to_playlist(absolute_path)
        self.send_vlc_command(self.PLAY_MEDIA)

    def play_files(self, paths):
        ''' Clear playlist, add new items from path array to playlist and play them. '''
        self.clear_playlist()
        for file in paths:
            #print(file)
            self.enqueue_to_playlist(file)
        self.send_vlc_command(self.PLAY_MEDIA)

    def stop_media(self):
        ''' Stop medialist '''
        self.send_vlc_command(self.STOP_MEDIA)

    def pause_file(self):
        ''' Toggle pause on/off '''
        self.send_vlc_command(self.PAUSE_FILE)

    def fast_forward(self):
        ''' Fast forward 10 secods'''
        self.send_vlc_command(self.HOTKEY_FAST_FORWARD)

    def rewind(self):
        ''' Rewind 10 secods'''
        self.send_vlc_command(self.HOTKEY_FAST_REWIND)

    def increase_volume(self):
        ''' Increase Vlc player volume doesn't affect system volume '''
        self.send_vlc_command(self.HOTKEY_VOLUME_INCREASE)

    def decrease_volume(self):
        ''' Decrease Vlc player volume doesn't affect system volume '''
        self.send_vlc_command(self.HOTKEY_VOLUME_DECREASE)

    def mute_volume(self):
        ''' Mute Vlc player volume doesn't affect system volume '''
        self.send_vlc_command(self.HOTKEY_VOLUME_MUTE)

    def add_to_playlist(self, path):
        '''Add item to playlist path should be absolute path'''
        command = "{} {}".format(self.ADD_TO_PLAYLIST, path)
        self.send_vlc_command(command)

    def enqueue_to_playlist(self, path):
        '''Enqueue item to playlist path should be absolute path'''
        command = "{} {}".format(self.ENQUEUE_TO_PLAYLIST, path)
        self.send_vlc_command(command)

    def clear_playlist(self):
        ''' Clear all the medias from current vlc medialist '''
        self.send_vlc_command(self.CLEAR_PLAYLIST)

    def cycle_audio_track(self):
        ''' Cycle through audio tracks '''
        self.send_vlc_command(self.HOTKEY_CYCLE_AUDIO)

    def cycle_subtitle_track(self):
        ''' Cycle through subtitle tracks '''
        self.send_vlc_command(self.HOTKEY_CYCLE_SUBTITLE)

    def play_previous_media(self):
        ''' Play previous media in medialist '''
        self.send_vlc_command(self.PLAY_PREVIOUS_MEDIA)

    def play_next_media(self):
        ''' Play next media in medialist '''
        self.send_vlc_command(self.PLAY_NEXT_MEDIA)

    def close_player(self):
        ''' Close vlc process and set self.vlcProsess to None '''
        self.vlc_process = None
        self.send_vlc_command(self.CLOSE_PLAYER)

    def get_currently_playing(self):
        '''Get title of currently playing media'''
        self.send_vlc_command("get_title", False)
        return self.__formated_socket_data()

    def __formated_socket_data(self) -> str:
        '''
        Get data from socket buffer, decode it and remove four last useless bytes
        that vlc rc module always writes to socket buffer
        '''
        buffer_data = self.__read_data_from_socket()
        buffer_string = buffer_data.decode(self.BUFFER_ENCODING)
        # remove "\t\n> " string from end
        return buffer_string[:-4]

    def __empty_reader_buffer(self):
        ''' Read data from buffer until there is data. This makes sure that buffer is empty '''
        while True:
            data = self.__read_data_from_socket()
            if not data:
                time.sleep(0.1)
            else:
                # Data found
                break

    def __read_data_from_socket(self) -> bytes:
        """ Try to read data from socket. Return empty bytes if no data currently in the buffer. """
        try:
            return self.vlc_socket.recv(self.BUFFER_BYTE_AMOUNT)
        except Exception as err:
            # No data
            pass
        return b''
