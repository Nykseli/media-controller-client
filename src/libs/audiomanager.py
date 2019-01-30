''' Functions for system master volume management '''
import libs.commands as commands
import errors


def increase_master_volume() -> dict:
    ''' Increase system master volume '''
    return commands.os_subprosses_handler("xdotool key XF86AudioRaiseVolume", errors.XDOTOOL_GENERAL)

def decrease_master_volume() -> dict:
    ''' Decrease system master volume '''
    return commands.os_subprosses_handler("xdotool key XF86AudioLowerVolume", errors.XDOTOOL_GENERAL)

def mute_master_volume() -> dict:
    ''' Mute system master volume '''
    return commands.os_subprosses_handler("xdotool key XF86AudioMute", errors.XDOTOOL_GENERAL)
