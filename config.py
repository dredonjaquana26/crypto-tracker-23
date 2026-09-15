import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class CryptoConfig:
    API_BASE: str = "https://api.coingecko.com/api/v3"
    TIMEOUT: int = 10
    SYMBOLS: tuple = ("bitcoin", "ethereum", "solana")
    DB_PATH: str = "crypto_data.sqlite"

def get_env_or_default(key: str, default: Any) -> Any:
    return os.getenv(key, default)

class ConfigFactory:
    _instances: Dict[str, Any] = {}

    @classmethod
    def fetch(cls) -> CryptoConfig:
        if 'core' not in cls._instances:
            cls._instances['core'] = CryptoConfig(
                API_BASE=get_env_or_default("API_URL", "https://api.coingecko.com/api/v3"),
                TIMEOUT=int(get_env_or_default("REQ_TIMEOUT", 10))
            )
        return cls._instances['core']

def load_settings() -> CryptoConfig:
    return ConfigFactory.fetch()