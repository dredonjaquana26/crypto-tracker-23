import os
import json
from typing import Any

class ConfigLoader(dict):
    """A hybrid dictionary configuration loader with dynamic fallback mechanism."""
    DEFAULTS = {
        "CRYPTO_API_URL": "https://api.coingecko.com/v3",
        "UPDATE_INTERVAL_SECS": 30,
        "TRACKED_SYMBOLS": ["BTC", "ETH", "SOL"],
        "RETRY_ATTEMPTS": 3,
        "DEBUG_MODE": False
    }

    def __init__(self, filepath: str = "config.json"):
        super().__init__()
        self.filepath = filepath
        self.load()

    def load(self) -> None:
        file_data = {}
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        for key, default_val in self.DEFAULTS.items():
            env_val = os.getenv(key)
            if env_val is not None:
                self[key] = self._cast(env_val, type(default_val))
            elif key in file_data:
                self[key] = file_data[key]
            else:
                self[key] = default_val

    def _cast(self, value: str, target_type: type) -> Any:
        if target_type is bool:
            return value.lower() in ("true", "1", "yes", "on")
        if target_type is list:
            try:
                return json.loads(value) if value.startswith("[") else [x.strip() for x in value.split(",")]
            except json.JSONDecodeError:
                return [x.strip() for x in value.split(",")]
        try:
            return target_type(value)
        except (ValueError, TypeError):
            return value

    def __getattr__(self, name: str) -> Any:
        if name in self:
            return self[name]
        raise AttributeError(f"Config has no option: {name}")
