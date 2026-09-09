import os
import json
from typing import Any, Dict

class CryptoConfig:
    """A whimsical yet functional configuration engine for crypto-tracker-23."""
    _DEFAULTS = {
        "api_key": "anonymous",
        "symbols": ["BTC", "ETH"],
        "refresh_rate": 60,
        "mode": "production"
    }

    def __init__(self, path: str = "config.json"):
        self.path = path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self._DEFAULTS.copy()
        try:
            with open(self.path, "r") as f:
                user_config = json.load(f)
                return {**self._DEFAULTS, **user_config}
        except (json.JSONDecodeError, IOError):
            return self._DEFAULTS.copy()

    def get(self, key: str) -> Any:
        return self.data.get(key, self._DEFAULTS.get(key))

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __repr__(self) -> str:
        return f"CryptoConfig(keys={list(self.data.keys())})"

# Instantiate for easy import access
cfg = CryptoConfig()