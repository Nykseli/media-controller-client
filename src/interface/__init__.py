'''
Interface helper user by modules in interface
'''
import time
import queue
import signal
import threading

# Name of the audio interface
AUDIO_INTERFACE = "audio"

# Name of the browser interface
BROWSER_INTERFACE = "browser"

# Name of the confgoi interface
CONFIG_INTERFACE = "config"

# Name of the general interface
GENERAL_INTERFACE = "general"

# Name of the keyboard interface
KEYBOARD_INTERFACE = "keyboard"

# Name of the mouse interface
MOUSE_INTERFACE = "mouse"

# Name of the vlc interface
VLC_INTERFACE = "vlc"


class InterfaceThread(threading.Thread):
    ''' Threading class that is used by interfaces '''

    def __init__(self, interface_name):
        super(InterfaceThread, self).__init__()
        self.setDaemon(True)
        self.name = interface_name + "_thread"
        self.queue = queue.Queue()
        self.kill = False
        self.timeout = 1 / 100 # Loop 100 times in second


    def run(self):
        while True:
            try:
                function, args, kwargs = self.queue.get(timeout=self.timeout)
                #print(str(type(args)))
                #print(str(type(*args)))
                if args and kwargs:
                    function(*args, kwargs)
                elif args:
                    function(*args)
                elif kwargs:
                    function(kwargs)
                else:
                    function()
            except queue.Empty:
                pass

            # self.kill is set by controller.py ProgrammerStopperClass
            # when program is closed
            if self.kill:
                break

            time.sleep(self.timeout)

    def add_to_queue(self, function, args: tuple = None, **kwargs):
        ''' Append function call to threads queue '''
        self.queue.put((function, args, kwargs))

    def call_return_function(self, function, args: tuple = None, **kwargs):
        ''' Use this function when you need return value from function call'''
        if args and kwargs:
            return function(*args, kwargs)
        if args:
            return function(*args)
        if kwargs:
            return function(kwargs)

        return function()
