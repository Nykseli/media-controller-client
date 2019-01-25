import errors
import interface
import messageobject
from interface import VLC_INTERFACE
from libs.vlcwrapper import VlcWrapper

__VLC_PLAYER = None
__ERROR_MESSGE = None

def __isVlcUsable():
    if __VLC_PLAYER:
        return True
    else:
        __ERROR_MESSGE = errors.error(errors.VLC_NOT_INIT)
    return False

def increaseVolume():
    '''Call VlcWrapper increaseVolume function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.increaseVolume)

def decreaseVolume():
    '''Call VlcWrapper decreaseVolume function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.decreaseVolume)

def muteVolume():
    '''Call VlcWrapper muteVolume function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.muteVolume)

def cycleAudioTrack():
    '''Call VlcWrapper cycleAudioTrack function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.cycleAudioTrack)

def cycleSubtitleTrack():
    '''Call VlcWrapper cycleSubtitleTrack function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.cycleSubtitleTrack)

def playFile(absolutePath):
    '''Call VlcWrapper playFile function'''

    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.playFile, (absolutePath, ))

def playFiles(absolutePaths):
    '''Call VlcWrapper playFiles function'''

    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.playFiles, (absolutePaths, ))

def playNextMedia():
    '''Call VlcWrapper playNextMedia function'''

    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.playNextMedia)

def playPreviousMedia():
    '''Call VlcWrapper playPreviousMedia function'''

    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.playPreviousMedia)

def pauseFile():
    '''Call VlcWrapper pauseFile function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.pauseFile)

def fastForward():
    ''' Call VlcWrapper fastForward function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.fastForward)

def rewind():
    ''' Call VlcWrapper rewind function'''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    __THREAD.addToQueue(__VLC_PLAYER.rewind)

def getCurrentlyPlaying():
    ''' Call VlcWrapper getCurrentlyPlaying function '''
    if not __isVlcUsable():
        return __ERROR_MESSGE

    currentlyPlaying = __THREAD.callReturnFunction(__VLC_PLAYER.getCurrentlyPlaying)
    #currentlyPlaying = __VLC_PLAYER.getCurrentlyPlaying()
    messagedata = {"currentlyPlaying" : currentlyPlaying}
    return messageobject.getMessageObject(VLC_INTERFACE, messagedata)

if __name__ == 'interface.vlc':
    # Vlc player needs to be initialized when vlc interface is imported
    # This means that vlc player should only be imported once
    __VLC_PLAYER = VlcWrapper()

    __THREAD = interface._InterfaceThread(interface.VLC_INTERFACE)
    __THREAD.start()
