'''
Functions for vlc interface
'''
import errors
import interface
import messageobject
from interface import VLC_INTERFACE
from libs.vlcwrapper import VlcWrapper

__VLC_PLAYER = None
__ERROR_MESSGE = None

def __vlc_error():
    ''' return False if no errors'''
    if __VLC_PLAYER:
        return False

    return errors.error(errors.VLC_NOT_INIT)

def increase_volume():
    '''Call VlcWrapper increase_volume function'''
    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.increase_volume)
    return False # No error message

def decrease_volume():
    '''Call VlcWrapper decrease_volume function'''
    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.decrease_volume)
    return False # No error message

def mute_volume():
    '''Call VlcWrapper mute_volume function'''
    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.mute_volume)
    return False # No error message

def cycle_audio_track():
    '''Call VlcWrapper cycle_audio_track function'''
    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.cycle_audio_track)
    return False # No error message

def cycle_subtitle_track():
    '''Call VlcWrapper cycle_subtitle_track function'''
    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.cycle_subtitle_track)
    return False # No error message

def play_file(absolute_path):
    '''Call VlcWrapper play_file function'''

    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.play_file, (absolute_path, ))
    return False # No error message

def stop_media():
    '''Call VlcWrapper stop_media function'''

    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.stop_media)
    return False # No error message

def play_files(absolute_paths):
    '''Call VlcWrapper play_files function'''

    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.play_files, (absolute_paths, ))
    return False # No error message

def play_next_media():
    '''Call VlcWrapper play_next_media function'''

    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.play_next_media)
    return False # No error message

def play_previous_media():
    '''Call VlcWrapper play_previous_media function'''

    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.play_previous_media)
    return False # No error message

def pause_file():
    '''Call VlcWrapper pause_file function'''
    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.pause_file)
    return False # No error message

def fast_forward():
    ''' Call VlcWrapper fast_forward function'''
    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.fast_forward)
    return False # No error message

def rewind():
    ''' Call VlcWrapper rewind function'''
    error = __vlc_error()
    if error:
        return error

    __THREAD.add_to_queue(__VLC_PLAYER.rewind)
    return False # No error message

def get_currently_playing():
    ''' Call VlcWrapper get_currently_playing function '''
    error = __vlc_error()
    if error:
        return error

    currently_playing = __THREAD.call_return_function(__VLC_PLAYER.get_currently_playing)
    #currentlyPlaying = __VLC_PLAYER.get_currently_playing()
    messagedata = {"currentlyPlaying" : currently_playing}
    return messageobject.get_message_object(VLC_INTERFACE, messagedata)

def init():
    global __VLC_PLAYER
    if __VLC_PLAYER:
        return

    __VLC_PLAYER = VlcWrapper()

    __THREAD = interface.InterfaceThread(interface.VLC_INTERFACE)
    __THREAD.start()
