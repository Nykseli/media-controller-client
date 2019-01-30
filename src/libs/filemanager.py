'''
filemanager contains class for managin files on device
'''
import os
import errors
from libs import VLC_CONFIG

#TODO: send error to user if absolute_path doesn't exists
def get_directories(absolute_path):
    ''' get list of directories in abslute_path '''
    directories = []
    for item in os.listdir(absolute_path):
        if os.path.isdir(os.path.join(absolute_path, item)):
            directories.append(item)
    directories.sort()
    return directories

def get_files(absolute_path):
    ''' get list of files in abslute_path '''
    files = []
    for item in os.listdir(absolute_path):
        if not os.path.isdir(os.path.join(absolute_path, item)):
            files.append(item)
    files.sort()
    return files

def is_filetype_allowed(file_name):
    '''
    Filted files according to config.json.
    The config is vlc.allowedFileTypes
    '''
    # If there is no vlc config at all. We can allow all filetypes
    if not VLC_CONFIG:
        return True
    # If allowedFileTypes is not defined. We can allow all filetypes
    if not VLC_CONFIG['allowedFileTypes']:
        return True

    file_type = file_name.split(".")[-1]
    if file_type in VLC_CONFIG['allowedFileTypes']:
        return True

    return False

def get_files_and_folders(absolute_path) -> dict:
    '''
    Get all files and folders form absolute_path in alphabetical order.
    Filter files according to config.json. Logic in is_filetype_allowed
    '''
    if not os.path.isdir(absolute_path):
        return errors.error(errors.FILE_NOT_FOUND)
    files_and_folders = {"files": [], "folders": [], "currentPath": absolute_path}
    for item in os.listdir(absolute_path):
        if not os.path.isdir(os.path.join(absolute_path, item)):
            if is_filetype_allowed(item):
                files_and_folders['files'].append(item)
        else:
            files_and_folders['folders'].append(item)

    files_and_folders['files'].sort()
    files_and_folders['folders'].sort()

    return files_and_folders
