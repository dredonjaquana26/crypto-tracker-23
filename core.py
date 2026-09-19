import functools
import time

class CryptoCache:
    def __init__(self, ttl_seconds=30):
        self.ttl = ttl_seconds
        self.cache = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in self.cache:
                data, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return data
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

@CryptoCache(ttl_seconds=60)
def fetch_market_price(symbol: str) -> float:
    # Simulate high latency network request
    time.sleep(0.5)
    prices = {'BTC': 65000.0, 'ETH': 3500.0, 'SOL': 140.0}
    return prices.get(symbol, 0.0)

def batch_process_prices(symbols: list):
    # Using list comprehension for speed optimization
    return {s: fetch_market_price(s) for s in symbols}

if __name__ == '__main__':
    # First call takes 0.5s, second call is instant
    start = time.perf_counter()
    print(batch_process_prices(['BTC', 'ETH']))
    print(f"Execution time: {time.perf_counter() - start:.4f}s")