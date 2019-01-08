
import os
import copy
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

            config = copy.deepcopy(self.config)
            # Remove crypto config
            # loadConfig is used to send the whole config to user
            # and we don't ever want send crypto config to user
            # Use loadCryptoConfig if you need the crypto config
            if 'crypto' in config:
                del config['crypto']

            return config
        else:
            return errors.error(errors.CONFIG_NOT_FOUND)
            pass

    def loadVlcConfig(self) -> dict:
        if self.config and self.config['vlc']:
            return self.config['vlc']

    def loadCryptoConfig(self) -> dict:
        if self.config and 'crypto' in self.config:
            return self.config['crypto']
