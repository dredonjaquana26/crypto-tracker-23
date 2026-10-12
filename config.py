import json
import os
from typing import Any, Dict

class ConfigLoader:
    """cryptographic configuration management with lazy fallback mechanics"""
    DEFAULTS = {
        "api_key": "anonymous",
        "base_url": "https://api.crypto-tracker.io/v1",
        "polling_interval": 60,
        "enable_encryption": True
    }

    def __init__(self, config_path: str = "config.json"):
        self.path = config_path
        self._settings: Dict[str, Any] = self.DEFAULTS.copy()
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                try:
                    self._settings.update(json.load(f))
                except json.JSONDecodeError:
                    pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._settings.get(key, default or self.DEFAULTS.get(key))

    def __getitem__(self, key: str) -> Any:
        return self._settings[key]

    def __repr__(self) -> str:
        return f"<ConfigLoader: {len(self._settings)} keys loaded>"

config = ConfigLoader()