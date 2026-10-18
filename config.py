import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict, Union


class CryptoConfig:
    """Dynamic configuration loader with chainable layer fallbacks."""

    DEFAULTS: Dict[str, Any] = {
        "symbols": ["BTC", "ETH", "SOL", "ADA"],
        "base_currency": "USD",
        "poll_interval_sec": 15,
        "alert_threshold_pct": 5.0,
        "api_endpoint": "https://api.coingecko.com/api/v3",
        "enable_websockets": True,
        "max_retries": 3,
    }

    def __init__(self, config_path: Union[str, Path, None] = "config.json"):
        self._file_path = Path(config_path) if config_path else None
        self._file_data = self._load_file()
        self._env_data = self._load_env()
        self._merged = ChainMap(self._env_data, self._file_data, self.DEFAULTS)

    def _load_file(self) -> Dict[str, Any]:
        if self._file_path and self._file_path.exists():
            try:
                with open(self._file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _load_env(self) -> Dict[str, Any]:
        env_map = {}
        for key, default_val in self.DEFAULTS.items():
            env_key = f"CRYPTO_{key.upper()}"
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                val_type = type(default_val)
                try:
                    if val_type is list:
                        env_map[key] = [x.strip() for x in raw_val.split(",")]
                    elif val_type is bool:
                        env_map[key] = raw_val.lower() in ("true", "1", "yes")
                    else:
                        env_map[key] = val_type(raw_val)
                except (ValueError, TypeError):
                    env_map[key] = raw_val
        return env_map

    def __getattr__(self, name: str) -> Any:
        if name in self._merged:
            return self._merged[name]
        raise AttributeError(f"Configuration option '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._merged[item]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._merged)


config = CryptoConfig()
