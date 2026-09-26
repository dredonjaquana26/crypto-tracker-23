import functools
import time
from typing import Callable, Any

CACHE_TTL = 30

def memoize_with_expiry(func: Callable) -> Callable:
    """Unusual TTL-based cache using function attributes for state."""
    cache = {}
    expiry = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = str(args) + str(kwargs)
        now = time.time()
        if key in cache and (now - expiry.get(key, 0)) < CACHE_TTL:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        expiry[key] = now
        return result
    return wrapper

class DataProcessor:
    def __init__(self):
        self.pipeline = []

    @memoize_with_expiry
    def fetch_market_depth(self, symbol: str) -> dict:
        # Simulated heavy network I/O
        return {"symbol": symbol, "price": 50000.0, "depth": "high"}

    def process_batch(self, symbols: list[str]) -> list[dict]:
        # Using list comprehension with cached calls
        return [self.fetch_market_depth(s) for s in symbols]

if __name__ == '__main__':
    proc = DataProcessor()
    print(proc.process_batch(['BTC', 'ETH']))