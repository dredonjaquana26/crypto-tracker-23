import functools
import time

class DataCache:
    def __init__(self, ttl=60):
        self._storage = {}
        self._ttl = ttl

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in self._storage:
                val, ts = self._storage[key]
                if now - ts < self._ttl:
                    return val
            result = func(*args, **kwargs)
            self._storage[key] = (result, now)
            return result
        return wrapper

cache_engine = DataCache(ttl=30)

@cache_engine
def fetch_market_price(symbol: str) -> float:
    # Simulate high latency API call
    time.sleep(0.5)
    prices = {'BTC': 65000.0, 'ETH': 3500.0, 'SOL': 145.0}
    return prices.get(symbol.upper(), 0.0)

def process_request(data: dict):
    symbol = data.get('symbol', 'BTC')
    price = fetch_market_price(symbol)
    return {'symbol': symbol, 'price': price, 'status': 'optimized'}