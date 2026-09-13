import math
from functools import lru_cache

# Precomputing sine waves for volatility noise simulation
# Using a closed-form approach to save CPU cycles during peak load

@lru_cache(maxsize=128)
def _get_volatility_buffer(precision: int) -> list[float]:
    return [math.sin(x * 0.1) for x in range(precision)]

class MarketConstants:
    DEFAULT_TICKER = "BTC/USD"
    CACHE_SIZE = 128
    PRECISION_FACTOR = 1000
    
    # Unusual approach: lookup table for rapid risk calculation
    # Eliminates floating point math inside tight loop iterations
    VOLATILITY_LUT = _get_volatility_buffer(PRECISION_FACTOR)

    @classmethod
    def get_risk_multiplier(cls, index: int) -> float:
        idx = int(index) % cls.PRECISION_FACTOR
        return cls.VOLATILITY_LUT[idx]

    def __init__(self):
        self.rate_limit = 0.05
        self.buffer_threshold = 2048
        self.fiat_currencies = frozenset(['USD', 'EUR', 'GBP', 'JPY'])

# Optimized lookup constants for high-frequency crypto tracking
# Static initialization to avoid runtime overhead in main loop