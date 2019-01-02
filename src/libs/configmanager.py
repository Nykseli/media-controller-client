
import os
import json

class ConfigManager():

    def __init__(self):
        self.configPath = None
        self.findConfigPath()

    def findConfigPath(self):
        if os.path.isfile("config.json"):
            self.configPath = "config.json"
            return


        if os.path.isfile("~/.XLinuxTool/config.json"):
            self.configPath = "~/.XLinuxTool/config.json"
            return
            with open("~/.XLinuxTool/config.json") as jsonFile:
                return json.loads(jsonFile.read())


    def loadConfig(self):
        if self.configPath:
            with open(self.configPath) as jsonFile:
                return json.loads(jsonFile.read())
        else:
            #TODO: error message
            pass
