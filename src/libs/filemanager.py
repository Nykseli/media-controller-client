import os
import errors
from libs import VLC_CONFIG

class FileManager():

    def __init__(self):
        pass

    #TODO: send error to user if absolutePath doesn't exists
    def getDirectories(self, absolutePath):
        directories = []
        for item in os.listdir(absolutePath):
            if os.path.isdir(os.path.join(absolutePath, item)):
                directories.append(item)
        directories.sort()
        return directories

    def getFiles(self, absolutePath):
        files = []
        for item in os.listdir(absolutePath):
            if not os.path.isdir(os.path.join(absolutePath, item)):
                files.append(item)
        files.sort()
        return files

    def isFileTypeAllowed(self, fileName):
        '''
        Filted files according to config.json.
        The config is vlc.allowedFileTypes
        '''
        # If there is no vlc config at all. We can allow all filetypes
        if not VLC_CONFIG:
            return True
        # If allowedFileTypes is not defined. We can allow all filetypes
        elif not VLC_CONFIG['allowedFileTypes']:
            return True

        fileType = fileName.split(".")[-1]
        if fileType in VLC_CONFIG['allowedFileTypes']:
            return True

        return False



    def getFilesAndFolders(self, absolutePath) -> dict:
        '''
        Get all files and folders form absolutepath in alphabetical order.
        Filter files according to config.json. Logic in isFileTypeAllowed
        '''
        if not os.path.isdir(absolutePath):
            return errors.error(errors.FILE_NOT_FOUND)

        filesAndFolders = {"files": [], "folders": [], "currentPath": absolutePath}

        for item in os.listdir(absolutePath):
            if not os.path.isdir(os.path.join(absolutePath, item)):
                if self.isFileTypeAllowed(item):
                    filesAndFolders['files'].append(item)
            else:
                filesAndFolders['folders'].append(item)

        filesAndFolders['files'].sort()
        filesAndFolders['folders'].sort()

        return filesAndFolders
