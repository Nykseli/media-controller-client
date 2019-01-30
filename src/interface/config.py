'''
Functions for config interface
'''

from libs import CONFIG

__CONFIG = None
__ERROR_MESSGE = None

def __config_error():
    ''' Return False if usable '''
    if __CONFIG:
        return False

    return {"error": "Config not initialized"}

def get_config():
    '''Call VlcWrapper playFile function'''
    error = __config_error()
    if error:
        return error

    return {"config": __CONFIG}

if __name__ == 'interface.config':
    # Vlc player needs to be initialized when vlc interface is imported
    # This means that vlc player should only be imported once
    __CONFIG = CONFIG

    #TODO: implement interface._InterfaceThreading when config has functions
    # that process something
