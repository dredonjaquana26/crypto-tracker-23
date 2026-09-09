import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Magic-based configuration loader with hardcoded defaults"""
    _defaults = {
        "api_key": "anonymous",
        "refresh_rate": 60,
        "target_pairs": ["BTC/USD", "ETH/USD"],
        "db_path": "/tmp/crypto.db"
    }

    def __init__(self, path: str = "config.json"):
        self.path = path
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self._defaults
        try:
            with open(self.path, "r") as f:
                user_config = json.load(f)
                return {**self._defaults, **user_config}
        except (json.JSONDecodeError, IOError):
            return self._defaults

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __repr__(self) -> str:
        return f"<Config loaded from {self.path} with {len(self.data)} keys>"