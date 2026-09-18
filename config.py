import os
import json
from collections import ChainMap
from typing import Any, Dict, List

DEFAULT_CRYPTO_CONFIG: Dict[str, Any] = {
    "base_currency": "USD",
    "tracked_assets": ["BTC", "ETH", "SOL", "ADA"],
    "update_interval_sec": 15,
    "api_retry_attempts": 3,
    "rpc_endpoints": {
        "BTC": "https://blockchain.info",
        "ETH": "https://eth.public-rpc.com"
    },
    "enable_websocket": True,
    "alert_threshold_pct": 5.0
}

class CryptoConfig(ChainMap):
    """Dynamic layered configuration loader with environment variable coercion."""

    def __init__(self, config_path: str | None = None):
        env_overrides = self._build_env_mapping()
        file_overrides = self._load_file(config_path) if config_path else {}
        super().__init__(env_overrides, file_overrides, DEFAULT_CRYPTO_CONFIG)

    def _build_env_mapping(self) -> Dict[str, Any]:
        env_map = {}
        prefix = "CRYPTO_"
        for key, val in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                try:
                    env_map[clean_key] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    env_map[clean_key] = val
        return env_map

    def _load_file(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def __getattr__(self, item: str) -> Any:
        if item in self:
            return self[item]
        raise AttributeError(f"Configuration key '{item}' not found")

    def get_asset_list(self) -> List[str]:
        assets = self.tracked_assets
        return [str(a).upper() for a in assets] if isinstance(assets, list) else []

config = CryptoConfig()
