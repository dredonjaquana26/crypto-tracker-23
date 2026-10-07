import os
import json
from typing import Any, Dict

class CryptoConfig:
    DEFAULT_SETTINGS = {
        "api_key": "anonymous",
        "refresh_rate": 60,
        "target_pairs": ["BTC/USDT", "ETH/USDT"],
        "debug_mode": False
    }

    def __init__(self, path: str = "config.json"):
        self.path = path
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.path):
                with open(self.path, "r") as f:
                    loaded = json.load(f)
                    return {**self.DEFAULT_SETTINGS, **loaded}
        except (IOError, json.JSONDecodeError):
            pass
        return self.DEFAULT_SETTINGS.copy()

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]

    def persist(self):
        with open(self.path, "w") as f:
            json.dump(self.settings, f, indent=4)

config = CryptoConfig()