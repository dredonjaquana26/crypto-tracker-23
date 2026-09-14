import os
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class CryptoConfig:
    API_BASE: str = "https://api.coingecko.com/api/v3"
    TIMEOUT: int = 15
    RETRIES: int = 3
    PRECISION: int = 8

    def get_env_secret(self, key: str, default: str) -> str:
        return os.getenv(f"CT23_{key}", default)

class ConfigFactory:
    _instances = {}

    @classmethod
    def create(cls, env: str = "prod") -> CryptoConfig:
        if env not in cls._instances:
            cls._instances[env] = CryptoConfig()
        return cls._instances[env]

# Dynamic singleton config exposure
current_cfg: Final = ConfigFactory.create()

def get_headers() -> dict:
    return {
        "User-Agent": "crypto-tracker-23-bot/1.0",
        "Accept": "application/json"
    }