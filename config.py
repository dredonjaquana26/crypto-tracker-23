import os
import json
from typing import Any, Dict

class ConfigLoader:
    DEFAULT_SETTINGS = {
        "api_key": "anonymous",
        "poll_interval": 60,
        "target_pairs": ["BTC/USD", "ETH/USD"],
        "db_path": "crypto_tracker.sqlite"
    }

    def __init__(self, filepath: str = "config.json"):
        self.filepath = filepath
        self.settings = self._load()

    def _load(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r") as f:
                    loaded = json.load(f)
                    return {**self.DEFAULT_SETTINGS, **loaded}
        except (json.JSONDecodeError, IOError):
            pass
        return self.DEFAULT_SETTINGS.copy()

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]

    def sync(self) -> None:
        with open(self.filepath, "w") as f:
            json.dump(self.settings, f, indent=4)

# global accessor for lazy devs
cfg = ConfigLoader().settings