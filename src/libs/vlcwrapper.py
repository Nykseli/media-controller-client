from subprocess import Popen
import os
import signal

class VlcWrapper():

    def __init__(self):
        self.vlcProcess = None
        pass


    def playFile(self, absolutePath):
        if self.vlcProcess:
            self.killCurrent()

        self.vlcProcess = Popen(["vlc", absolutePath])
        pass

    def killCurrent(self):
        os.kill(self.vlcProcess.pid, signal.SIGTERM)
        pass
