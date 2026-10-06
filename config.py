import os
import json
from typing import get_type_hints, Any

class CryptoConfig:
    # Default configuration values
    API_URL: str = "https://api.coingecko.com/api/v3"
    TRACKED_COINS: list = ["bitcoin", "ethereum", "solana"]
    UPDATE_INTERVAL_SEC: int = 60
    ENABLE_TELEGRAM_ALERTS: bool = False
    PORTFOLIO_MIN_VALUE_USD: float = 100.0

    def __init__(self) -> None:
        self._load_config()

    def _cast_value(self, value: str, target_type: Any) -> Any:
        if target_type is bool:
            return value.lower() in ("true", "1", "yes")
        if target_type is list or getattr(target_type, "__origin__", None) is list:
            return [item.strip() for item in value.split(",") if item.strip()]
        try:
            return target_type(value)
        except (TypeError, ValueError):
            return value

    def _load_config(self) -> None:
        hints = get_type_hints(self.__class__)
        for key, target_type in hints.items():
            env_val = os.getenv(f"CRYPTO_{key}")
            if env_val is not None:
                parsed = self._cast_value(env_val, target_type)
                setattr(self, key, parsed)
            else:
                if not hasattr(self, key):
                    setattr(self, key, getattr(self.__class__, key))

    def to_dict(self) -> dict:
        return {k: getattr(self, k) for k in get_type_hints(self.__class__)}
