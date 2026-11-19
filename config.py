import os
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults
        self._load_env()

    def _load_env(self) -> None:
        for key in self._data.keys():
            env_val = os.getenv(f'CRYPTO_{key.upper()}')
            if env_val:
                self._data[key] = type(self._data[key])(env_val)

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

def get_settings() -> CryptoConfig:
    defaults = {
        'api_key': 'default_secret',
        'timeout': 30,
        'base_url': 'https://api.crypto-tracker-23.io',
        'retries': 3,
        'debug': False
    }
    return CryptoConfig(defaults)

settings = get_settings()