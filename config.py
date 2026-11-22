import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class CryptoConfig:
    API_KEY: str = os.getenv('CRYPTO_API_KEY', 'default_dev_key')
    BASE_URL: str = 'https://api.coingecko.com/api/v3'
    POLL_INTERVAL: int = int(os.getenv('POLL_INTERVAL', '60'))
    ENABLED_SYMBOLS: tuple = ('bitcoin', 'ethereum', 'solana')

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('__')}

def load_settings():
    return CryptoConfig()