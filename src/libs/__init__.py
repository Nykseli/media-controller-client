
from libs.configmanager import ConfigManager

config = ConfigManager()
CONFIG = config.loadConfig()
VLC_CONFIG = config.loadVlcConfig()
CRYPTO_CONFIG = config.loadCryptoConfig()
GENERAL_CONFIG = config.loadGeneralConfig()
WEBSOCKET_CONFIG = config.loadWebSocketConfig()
