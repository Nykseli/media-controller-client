"""
libs init module
"""
from libs.configmanager import ConfigManager

config = ConfigManager()
CONFIG = config.load_config()
VLC_CONFIG = config.load_vlc_config()
CRYPTO_CONFIG = config.load_crypto_config()
GENERAL_CONFIG = config.load_general_config()
WEBSOCKET_CONFIG = config.load_web_socket_config()
