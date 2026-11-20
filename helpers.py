import json
import os
from typing import Any, Dict

def load_crypto_config(path: str = "config.json") -> Dict[str, Any]:
    """Reads config with fallback defaults for crypto operations."""
    defaults = {
        "api_key": "dev_key_001",
        "base_currency": "USD",
        "refresh_rate": 60,
        "trading_pairs": ["BTC/USD", "ETH/USD"]
    }
    
    if not os.path.exists(path):
        return defaults

    try:
        with open(path, "r") as f:
            user_config = json.load(f)
            # Deep merge strategy for nested defaults
            return {**defaults, **user_config}
    except (json.JSONDecodeError, IOError):
        return defaults

class ConfigProxy:
    """Magic access to config settings via object attributes."""
    def __init__(self, settings: Dict[str, Any]):
        self._data = settings

    def __getattr__(self, item: str) -> Any:
        return self._data.get(item)

def get_app_settings() -> ConfigProxy:
    """Factory for config proxy instance."""
    return ConfigProxy(load_crypto_config())