
#General errors
UNKNOWN_ERROR = "Unknown error!"
FILE_NOT_FOUND = "File doesn't exists!"
CONFIG_NOT_FOUND = "Config file not found!"

# xdotool errors
XDOTOOL_GENERAL = "xdotool error!"

# Vlc errors
VLC_CANNOT_PLAY = "Vlc cannot play the requested file!"

def error(error) -> dict:
    return {"error": error}
