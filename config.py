import os
import json
from typing import Any, Dict

class CryptoConfig:
    _DEFAULTS = {
        "api_key": "anonymous",
        "base_currency": "USD",
        "refresh_interval": 60,
        "endpoints": ["binance", "coinbase"]
    }

    def __init__(self, path: str = "config.json"):
        self._path = path
        self._data = self._load_from_disk()

    def _load_from_disk(self) -> Dict[str, Any]:
        if not os.path.exists(self._path):
            return self._DEFAULTS
        try:
            with open(self._path, "r") as f:
                loaded = json.load(f)
                return {**self._DEFAULTS, **loaded}
        except (json.JSONDecodeError, IOError):
            return self._DEFAULTS

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default or self._DEFAULTS.get(key))

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"CryptoConfig({self._data})"

settings = CryptoConfig()