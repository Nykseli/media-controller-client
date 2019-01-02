import os


class AudioManager():

    def __init__(self):
        pass

    def increaseMasterVolume(self):
        os.system("xdotool key XF86AudioRaiseVolume")

    def decreaseMasterVolume(self):
        os.system("xdotool key XF86AudioLowerVolume")

    def muteMasterVolume(self):
        os.system("xdotool key XF86AudioMute")
