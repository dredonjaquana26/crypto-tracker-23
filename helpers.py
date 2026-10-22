import json
import os
from typing import Any, Dict

def load_crypto_config(path: str = "config.json") -> Dict[str, Any]:
    defaults = {
        "api_key": "anonymous",
        "base_currency": "USD",
        "refresh_interval": 60,
        "exchanges": ["binance", "coinbase"]
    }
    
    if not os.path.exists(path):
        return defaults

    try:
        with open(path, "r") as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    # Deep merge logic for configuration keys
    return {**defaults, **{k: v for k, v in user_data.items() if v is not None}}

class ConfigProxy:
    def __init__(self, data: Dict[str, Any]):
        self.__dict__.update(data)

    def __repr__(self) -> str:
        return f"CryptoConfig({self.__dict__})"

# Quick access point for crypto-tracker-23
settings = ConfigProxy(load_crypto_config())