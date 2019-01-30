'''
Config manager class manages config.json
'''
import os
import copy
import json
import errors

class ConfigManager():
    ''' Class for config.json management '''
    def __init__(self):
        self.config_path = None
        self.config = None
        self.find_config_path()

    def find_config_path(self):
        ''' set self.config_path if config is found '''
        if os.path.isfile("config.json"):
            self.config_path = "config.json"
            return


        if os.path.isfile("~/.MediaControllerClient/config.json"):
            self.config_path = "~/.MediaControllerClient/config.json"
            return


    def load_config(self) -> dict:
        '''
        Load almost the whole config.
        This returns dict that contains all the config data that we want to send to client
        '''
        if self.config_path:
            with open(self.config_path) as jsonFile:
                self.config = json.loads(jsonFile.read())

            config = copy.deepcopy(self.config)
            # Remove crypto config
            # load_config is used to send the whole config to user
            # and we don't ever want send crypto config to user
            # Use loadCryptoConfig if you need the crypto config
            if 'crypto' in config:
                del config['crypto']

            # Remove websocet for the same reason as crypto
            if 'websocket' in config:
                del config['websocket']

            return config
        return errors.error(errors.CONFIG_NOT_FOUND)

    def load_vlc_config(self) -> dict:
        ''' Load only the vlc part of the config '''
        if self.config and self.config['vlc']:
            return self.config['vlc']
        return None # Return None if config is not found

    def load_crypto_config(self) -> dict:
        ''' Load only the crypto part of the config '''
        if self.config and 'crypto' in self.config:
            return self.config['crypto']
        return None # Return None if config is not found


    def load_web_socket_config(self) -> dict:
        ''' Load only the web socket part of the config '''
        if self.config and 'websocket' in self.config:
            return self.config['websocket']
        return None # Return None if config is not found

    def load_general_config(self) -> dict:
        ''' Load only the general part of the config '''
        if self.config and 'general' in self.config:
            return self.config['general']
        return None # Return None if config is not found
