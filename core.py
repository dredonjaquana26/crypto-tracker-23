import time
import functools
from typing import Callable, Any

CACHE_TTL = 30
_memo_store = {}

def memoize_crypto_data(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        key = f"{func.__name__}:{args}:{frozenset(kwargs.items())}"
        now = time.monotonic()
        if key in _memo_store:
            val, expiry = _memo_store[key]
            if now < expiry:
                return val
        result = func(*args, **kwargs)
        _memo_store[key] = (result, now + CACHE_TTL)
        return result
    return wrapper

class PriceAggregator:
    def __init__(self, tickers: list):
        self.tickers = tickers

    @memoize_crypto_data
    def fetch_market_depth(self, symbol: str) -> dict:
        # Simulate high-latency network IO to exchange API
        time.sleep(0.5)
        return {"symbol": symbol, "bid": 50000.0, "ask": 50005.0, "ts": time.time()}

    def bulk_fetch(self) -> list:
        return [self.fetch_market_depth(t) for t in self.tickers]

if __name__ == '__main__':
    agg = PriceAggregator(['BTC', 'ETH'])
    print(agg.bulk_fetch())
    print(agg.bulk_fetch())