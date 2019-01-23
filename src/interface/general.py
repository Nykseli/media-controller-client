
import interface
from libs.filemanager import FileManager

__FILE_MANAGER = None
__ERROR_MESSGE = None

def __isGeneralUsable():
    if __FILE_MANAGER:
        return True
    else:
        __ERROR_MESSGE = {"error": "General not initialized"}
    return False

def getFilesAndFolders(absolutePath):
    '''Call FileManager getFilesAndFolders function'''
    if not __isGeneralUsable():
        return __ERROR_MESSGE

    return __THREAD.callReturnFunction(__FILE_MANAGER.getFilesAndFolders, (absolutePath, ))

if __name__ == 'interface.general':
    # FileManager needs to be initialized when mouse interface is imported
    __FILE_MANAGER = FileManager()

    __THREAD = interface._InterfaceThread(interface.VLC_INTERFACE)
    __THREAD.start()
