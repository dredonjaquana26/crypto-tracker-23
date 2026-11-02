import functools
import time
from typing import Dict, Any

CACHE_TTL = 30
_INTERNAL_CACHE: Dict[str, tuple[float, Any]] = {}

def memoize_crypto_data(func):
    @functools.wraps(func)
    def wrapper(symbol: str, *args, **kwargs):
        now = time.time()
        if symbol in _INTERNAL_CACHE:
            timestamp, result = _INTERNAL_CACHE[symbol]
            if now - timestamp < CACHE_TTL:
                return result
        
        result = func(symbol, *args, **kwargs)
        _INTERNAL_CACHE[symbol] = (now, result)
        return result
    return wrapper

class CryptoProcessor:
    def __init__(self, exchange: str):
        self.exchange = exchange

    @memoize_crypto_data
    def fetch_price(self, symbol: str) -> float:
        # Simulated heavy network I/O
        time.sleep(0.5)
        price_map = {'BTC': 65000.0, 'ETH': 3500.0, 'SOL': 145.0}
        return price_map.get(symbol.upper(), 0.0)

    def batch_process(self, symbols: list[str]) -> dict[str, float]:
        results = {}
        for s in symbols:
            results[s] = self.fetch_price(s)
        return results