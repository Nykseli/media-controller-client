from libs.vlcwrapper import VlcWrapper

__VLC_PLAYER = None
__ERROR_MESSGE = None

def __isVlcUsable():
    if __VLC_PLAYER:
        return True
    else:
        __ERROR_MESSGE = {"error": "Vlc player not initialized"}
    return False

def playFile(absolutePath):
    '''Call VlcWrapper playFile function'''

    if not __isVlcUsable():
        return __ERROR_MESSGE

    return __VLC_PLAYER.playFile(absolutePath)

def pauseFile():
    '''Call VlcWrapper pauseFile function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    return __VLC_PLAYER.pauseFile()


if __name__ == 'interface.vlc':
    # Vlc player needs to be initialized when vlc interface is imported
    # This means that vlc player should only be imported once
    __VLC_PLAYER = VlcWrapper()

