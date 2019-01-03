import os
import libs.commands as commands
import errors

class AudioManager():

    def __init__(self):
        pass

    def increaseMasterVolume(self) -> dict:
        return commands.osSystemHanlder("xdotool key XF86AudioRaiseVolume", errors.XDOTOOL_GENERAL)

    def decreaseMasterVolume(self) -> dict:
        return commands.osSystemHanlder("xdotool key XF86AudioLowerVolume", errors.XDOTOOL_GENERAL)

    def muteMasterVolume(self) -> dict:
        return commands.osSystemHanlder("xdotool key XF86AudioMute", errors.XDOTOOL_GENERAL)
