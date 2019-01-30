'''
Functions for audio interface
'''

import interface
import libs.audiomanager as __AUDIO_MANAGER


def __audio_error():
    ''' Return False if usable '''
    # TODO: config for disabling audio

    return False

def decrease_master_volume():
    '''Call AudioManager decrease_master_volume function'''
    error = __audio_error()
    if error:
        return error

    __THREAD.add_to_queue(__AUDIO_MANAGER.decrease_master_volume)
    return None # We dont want to return anything

def increase_master_volume():
    '''Call AudioManager increase_master_volume function'''
    error = __audio_error()
    if error:
        return error

    __THREAD.add_to_queue(__AUDIO_MANAGER.increase_master_volume)
    return None # We dont want to return anything

def mute_master_volume():
    '''Call AudioManager mute_master_volume function'''
    error = __audio_error()
    if error:
        return error

    __THREAD.add_to_queue(__AUDIO_MANAGER.mute_master_volume)
    return None # We dont want to return anything

if __name__ == 'interface.audio':
    __THREAD = interface.InterfaceThread(interface.AUDIO_INTERFACE)
    __THREAD.start()
