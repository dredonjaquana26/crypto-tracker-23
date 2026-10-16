import sys
from functools import lru_cache

# Using a lazy-loading proxy approach to avoid memory bloat
# at application startup in low-spec containers

class ConfigRegistry:
    _cache = {}

    def __getattr__(self, name):
        if name not in self._cache:
            self._cache[name] = self._load_from_vault(name)
        return self._cache[name]

    def _load_from_vault(self, key):
        mapping = {
            "TICKER_REFRESH": 0.5,
            "MAX_RETRIES": 3,
            "PRECISION_LIMIT": 8,
            "CRYPTO_ENDPOINTS": [
                "wss://stream.binance.com:9443/ws",
                "wss://api.exchange.coinbase.com/",
            ],
            "SIGNATURE_SALT": b'super-secret-salt-crypto-23'
        }
        return mapping.get(key)

@lru_cache(maxsize=None)
def get_constant(key: str):
    return ConfigRegistry().__getattr__(key)

# Exposing constants via a read-only slot-like structure for performance
class CryptoConstants:
    __slots__ = ('REFRESH', 'RETRIES')
    def __init__(self):
        self.REFRESH = get_constant("TICKER_REFRESH")
        self.RETRIES = get_constant("MAX_RETRIES")

CONSTANTS = CryptoConstants()