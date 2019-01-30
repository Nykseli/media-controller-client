'''
Functions for general interface
'''
import interface
import libs.filemanager as filemanager

__FILE_MANAGER = True
__ERROR_MESSGE = None

def __general_error():
    if __FILE_MANAGER:
        return False

    return {"error": "General not initialized"}

def get_files_and_folders(absolute_path):
    '''Call FileManager get_files_and_folders function'''
    error = __general_error()
    if error:
        return error

    return __THREAD.call_return_function(filemanager.get_files_and_folders, (absolute_path, ))

if __name__ == 'interface.general':
    # FileManager needs to be initialized when mouse interface is imported

    __THREAD = interface.InterfaceThread(interface.GENERAL_INTERFACE)
    __THREAD.start()
