import os


class AudioManager():

    def __init__(self):
        pass

    def increaseMasterVolume(self):
        os.system("amixer set 'Master' 5%+")

    def decreaseMasterVolume(self):
        os.system("amixer set 'Master' 5%-")
