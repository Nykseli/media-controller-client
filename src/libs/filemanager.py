import os

class FileManager():

    def __init__(self):
        pass


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

    def getFilesAndFolders(self, absolutePath):
        filesAndFolders = {"files": [], "folders": [], "currentPath": absolutePath}

        for item in os.listdir(absolutePath):
            if not os.path.isdir(os.path.join(absolutePath, item)):
                filesAndFolders['files'].append(item)
            else:
                filesAndFolders['folders'].append(item)

        filesAndFolders['files'].sort()
        filesAndFolders['folders'].sort()

        return filesAndFolders
