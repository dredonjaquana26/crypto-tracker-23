import os
import json
from typing import Any

class ConfigLoader:
    API_URL: str = "https://api.coingecko.com/api/v3"
    UPDATE_INTERVAL_SEC: int = 60
    TRACKED_COINS: list = ["bitcoin", "ethereum", "solana"]
    DEBUG_MODE: bool = False

    def __init__(self, filepath: str = "config.json"):
        self._file_data = {}
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    self._file_data = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_") or name not in ConfigLoader.__annotations__:
            return super().__getattribute__(name)

        default_val = getattr(ConfigLoader, name)
        expected_type = type(default_val)

        val = os.environ.get(f"CRYPTO_{name}")
        if val is None:
            val = self._file_data.get(name, default_val)

        return self._cast(val, expected_type)

    def _cast(self, val: Any, target_type: type) -> Any:
        if isinstance(val, target_type):
            return val
        if target_type is bool:
            return str(val).lower() in ("true", "1", "yes", "on")
        if target_type is list and isinstance(val, str):
            return [item.strip() for item in val.split(",") if item.strip()]
        try:
            return target_type(val)
        except (ValueError, TypeError):
            return val