
from libs.configmanager import ConfigManager

config = ConfigManager()
CONFIG = config.loadConfig()
VLC_CONFIG = config.loadVlcConfig()
CRYPTO_CONFIG = config.loadCryptoConfig()
WEBSOCKET_CONFIG = config.loadWebSocketConfig()
