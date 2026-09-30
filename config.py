import os
import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    """Crypto-tracker-23 configuration engine with emergency defaults."""
    
    DEFAULTS = {
        "api_key": "none",
        "refresh_interval": 60,
        "endpoints": ["binance", "coinbase"],
        "debug_mode": False
    }

    def __init__(self, config_path: str = "config.json"):
        self.path = Path(config_path)
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return self.DEFAULTS
        try:
            with open(self.path, "r") as f:
                user_cfg = json.load(f)
            return {**self.DEFAULTS, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return self.DEFAULTS

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._data.get(key, fallback or self.DEFAULTS.get(key))

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    @property
    def all(self) -> Dict[str, Any]:
        return self._data