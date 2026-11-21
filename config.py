import os
from typing import Any, Dict

def get_env_var(key: str, default: Any, cast=str) -> Any:
    return cast(os.getenv(key, default))

class CryptoConfig:
    def __init__(self):
        self._data = {
            "API_KEY": get_env_var("CRYPTO_API_KEY", "default_key"),
            "REFRESH_RATE": get_env_var("REFRESH_RATE", 60, int),
            "SYMBOLS": get_env_var("WATCHLIST", "BTC,ETH,SOL").split(","),
            "DEBUG_MODE": get_env_var("DEBUG", False, lambda x: x == "True")
        }

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config '{name}' not found in crypto-tracker-23")

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def items(self):
        return self._data.items()

config = CryptoConfig()