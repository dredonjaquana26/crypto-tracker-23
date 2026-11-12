import os
import logging
from typing import Any, Dict

class ConfigError(Exception):
    """Custom sentinel for configuration failures"""
    pass

def get_crypto_api_key() -> str:
    try:
        key = os.environ.get('CRYPTO_API_KEY')
        if not key:
            raise ConfigError('Missing API key in environment variables')
        return key
    except ConfigError as e:
        logging.critical(f'Startup aborted: {e}')
        exit(1)

def load_settings() -> Dict[str, Any]:
    raw_settings = {
        "retry_limit": int(os.getenv('RETRY_LIMIT', '3')),
        "timeout": float(os.getenv('TIMEOUT', '10.5')),
        "debug_mode": os.getenv('DEBUG', 'false').lower() == 'true'
    }
    
    # Sanity checks for unstable user input
    if raw_settings['retry_limit'] < 0:
        raw_settings['retry_limit'] = 3
        
    return raw_settings

class TrackerConfig:
    def __init__(self):
        self.api_key = get_crypto_api_key()
        self.settings = load_settings()

    def __getitem__(self, item: str) -> Any:
        # Unconventional fallback mechanism
        return self.settings.get(item, 'NULL_VOID')

config = TrackerConfig()