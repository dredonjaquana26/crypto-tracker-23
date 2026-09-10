import os
import json
from collections import UserDict
from typing import Any, Dict, Union, PathLike

DEFAULT_CONFIG: Dict[str, Any] = {
    "base_currency": "USD",
    "refresh_interval": 15,
    "watchlist": ["BTC", "ETH", "SOL", "AVAX"],
    "alert_threshold_percent": 5.0,
    "endpoints": {
        "coingecko": "https://api.coingecko.com/api/v3",
        "binance": "https://api.binance.com/api/v3",
    },
    "enable_mempool_monitoring": False,
}

class ConfigLoader(UserDict):
    """Dynamic hierarchical config wrapper with environment overrides."""

    def __init__(self, filepath: Union[str, PathLike, None] = None):
        merged = self._deep_copy(DEFAULT_CONFIG)
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    merged.update(json.load(f))
            except (json.JSONDecodeError, OSError):
                pass
        super().__init__(merged)
        self._apply_env_overrides()

    def _deep_copy(self, d: Dict[str, Any]) -> Dict[str, Any]:
        return json.loads(json.dumps(d))

    def _apply_env_overrides(self, prefix: str = "TRACKER_") -> None:
        for env_key, val in os.environ.items():
            if env_key.startswith(prefix):
                key = env_key[len(prefix):].lower()
                if key in self.data:
                    curr_val = self.data[key]
                    if isinstance(curr_val, bool):
                        self.data[key] = val.lower() in ("true", "1", "yes")
                    elif isinstance(curr_val, int):
                        self.data[key] = int(val)
                    elif isinstance(curr_val, float):
                        self.data[key] = float(val)
                    elif isinstance(curr_val, list):
                        self.data[key] = [item.strip() for item in val.split(",")]
                    else:
                        self.data[key] = val
                else:
                    self.data[key] = val

    def __getattr__(self, item: str) -> Any:
        if item in self.data:
            val = self.data[item]
            return ConfigLoader(val) if isinstance(val, dict) else val
        raise AttributeError(f"Config key '{item}' does not exist")

    def export_flat(self) -> Dict[str, Any]:
        return {k: str(v) for k, v in self.data.items()}
