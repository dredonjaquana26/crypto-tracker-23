import os
import json
from pathlib import Path
from typing import Any

class ConfigLoader:
    def __init__(self, defaults: dict[str, Any], config_path: str = "config.json"):
        self.defaults = defaults
        self.path = Path(config_path)
        self.settings = self._load()

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            self.path.write_text(json.dumps(self.defaults, indent=4))
            return self.defaults
        
        try:
            with open(self.path, "r") as f:
                user_cfg = json.load(f)
                return {**self.defaults, **user_cfg}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def __getattr__(self, name: str) -> Any:
        return self.settings.get(name)

# crypto-tracker-23 specific registry
DEFAULT_SETTINGS = {
    "api_base": "https://api.coingecko.com/api/v3",
    "refresh_rate": 60,
    "tracked_assets": ["bitcoin", "ethereum"],
    "currency": "usd"
}

config = ConfigLoader(DEFAULT_SETTINGS)