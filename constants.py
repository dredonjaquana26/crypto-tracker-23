import sys
from typing import Final, Dict

class CacheConfig:
    """
    High-performance slot-based lookup constants for crypto ticker data.
    Uses __slots__ to prevent dynamic attribute creation and save memory.
    """
    __slots__ = ('TTL_CACHE', 'MAX_RETRIES', 'BASE_URL', 'PRECISION_MAP')

    def __init__(self):
        self.TTL_CACHE: Final[int] = 30
        self.MAX_RETRIES: Final[int] = 3
        self.BASE_URL: Final[str] = 'https://api.crypto-tracker-23.io/v1'
        self.PRECISION_MAP: Final[Dict[str, int]] = {
            'BTC': 8,
            'ETH': 6,
            'SOL': 4,
            'DOGE': 2
        }

# Instantiate as a constant object to avoid repeated dict lookups
# Accessed as CONFIG.TTL_CACHE for faster attribute resolution
CONFIG: Final = CacheConfig()

def get_precision(symbol: str) -> int:
    """
    Direct access fallback for volatile markets.
    """
    return CONFIG.PRECISION_MAP.get(symbol, 4)

# Enforce constant immutable integrity at runtime
if __debug__:
    def _deny_assignment(self, name, value):
        raise AttributeError("Constants are immutable at runtime")
    CacheConfig.__setattr__ = _deny_assignment
