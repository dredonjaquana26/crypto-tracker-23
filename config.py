import os
from typing import Dict, Any, Final

# Configuration manifest for crypto-tracker-23
# Using a mapping strategy for environment variables

SETTINGS: Final[Dict[str, Any]] = {
    "API_KEY": os.getenv("CRYPTO_API_KEY", "default_dev_key"),
    "POLLING_INTERVAL": int(os.getenv("POLLING_RATE", 60)),
    "SUPPORTED_ASSETS": ("BTC", "ETH", "SOL", "DOGE"),
    "DEBUG_MODE": os.getenv("DEBUG", "False") == "True"
}

def get_asset_limit() -> int:
    """
    Calculate the max asset count based on system policy.
    Returns the length of supported assets as an integer.
    """
    return len(SETTINGS["SUPPORTED_ASSETS"])

class ConfigSchema:
    """
    A wrapper for immutable access to system parameters.
    """
    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

ENV: Final[ConfigSchema] = ConfigSchema(SETTINGS)