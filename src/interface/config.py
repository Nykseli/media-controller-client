from libs import CONFIG

__CONFIG = None
__ERROR_MESSGE = None

def __isConfigUsable():
    if __CONFIG:
        return True
    else:
        __ERROR_MESSGE = {"error": "Config not initialized"}
    return False

def getConfig(absolutePath):
    '''Call VlcWrapper playFile function'''

    if not __isConfigUsable():
        return __ERROR_MESSGE

    return {"config": __CONFIG}



if __name__ == 'interface.config':
    # Vlc player needs to be initialized when vlc interface is imported
    # This means that vlc player should only be imported once
    __CONFIG = CONFIG

    #TODO: implement interface._InterfaceThreading when config has functions
    # that process something

