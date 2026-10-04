import os
import json
from typing import Any, Dict

class ConfigLoader:
    """A slightly obsessive, non-standard config loader."""
    def __init__(self, defaults: Dict[str, Any], path: str = "config.json"):
        self._defaults = defaults
        self._path = path
        self.data = self._initialize()

    def _initialize(self) -> Dict[str, Any]:
        if not os.path.exists(self._path):
            self._save(self._defaults)
            return self._defaults
        
        try:
            with open(self._path, 'r') as f:
                user_data = json.load(f)
                return {**self._defaults, **user_data}
        except (json.JSONDecodeError, IOError):
            return self._defaults

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self._path, 'w') as f:
            json.dump(data, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

def load_crypto_config() -> ConfigLoader:
    defaults = {
        "api_key": "none",
        "refresh_interval": 60,
        "target_coins": ["BTC", "ETH", "SOL"],
        "db_path": "crypto_data.db"
    }
    return ConfigLoader(defaults)