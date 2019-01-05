from libs.audiomanager import AudioManager

__AUDIO_MANAGER = None
__ERROR_MESSGE = None

def __isAudioUsable():
    if __AUDIO_MANAGER:
        return True
    else:
        __ERROR_MESSGE = {"error": "Audio not initialized"}
    return False

def decreaseMasterVolume():
    '''Call AudioManager decreaseMasterVolume function'''
    if not __isAudioUsable():
        return __ERROR_MESSGE

    return __AUDIO_MANAGER.decreaseMasterVolume()

def increaseMasterVolume():
    '''Call AudioManager increaseMasterVolume function'''
    if not __isAudioUsable():
        return __ERROR_MESSGE

    return __AUDIO_MANAGER.increaseMasterVolume()

def muteMasterVolume():
    '''Call AudioManager muteMasterVolume function'''
    if not __isAudioUsable():
        return __ERROR_MESSGE

    return __AUDIO_MANAGER.muteMasterVolume()

if __name__ == 'interface.audio':
    # AudioManager needs to be initialized when mouse interface is imported
    __AUDIO_MANAGER = AudioManager()
