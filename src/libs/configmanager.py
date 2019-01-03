
import os
import json
import errors

class ConfigManager():

    def __init__(self):
        self.configPath = None
        self.config = None
        self.findConfigPath()

    def findConfigPath(self):
        if os.path.isfile("config.json"):
            self.configPath = "config.json"
            return


        if os.path.isfile("~/.MediaControllerClient/config.json"):
            self.configPath = "~/.MediaControllerClient/config.json"
            return


    def loadConfig(self) -> dict:
        if self.configPath:
            with open(self.configPath) as jsonFile:
                self.config = json.loads(jsonFile.read())
                return self.config
        else:
            return errors.error(errors.CONFIG_NOT_FOUND)
            pass

    def loadVlcConfig(self) -> dict:
        if self.config and self.config['vlc']:
            return self.config['vlc']

