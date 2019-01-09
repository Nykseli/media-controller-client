
#General errors
UNKNOWN_ERROR = "Unknown error!"
FILE_NOT_FOUND = "File doesn't exists!"
CONFIG_NOT_FOUND = "Config file not found!"

# xdotool errors
XDOTOOL_GENERAL = "xdotool error!"

# Keyboard errors
KEYBOARD_NOT_INIT = "Keyboard is not initialized"

# Vlc errors
VLC_CANNOT_PLAY = "Vlc cannot play the requested file!"
VLC_NOT_INIT = "Vlc player not initialized"


def error(error) -> dict:
    return {"error": error}


def printError(error):
    pass
