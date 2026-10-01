import functools
import time
from typing import Dict, Any

class CryptoCache:
    def __init__(self, ttl: int = 60):
        self.ttl = ttl
        self.storage: Dict[str, tuple[float, Any]] = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            now = time.monotonic()
            if key in self.storage:
                timestamp, result = self.storage[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.storage[key] = (now, result)
            return result
        return wrapper

@CryptoCache(ttl=30)
def fetch_price(symbol: str) -> float:
    # Simulated latency for crypto exchange API
    time.sleep(0.5)
    return 42069.13

class DataEngine:
    def __init__(self):
        self.registry = {}

    def get_market_data(self, symbol: str) -> float:
        return fetch_price(symbol)

    def batch_process(self, symbols: list):
        return {s: self.get_market_data(s) for s in symbols}

if __name__ == "__main__":
    engine = DataEngine()
    print(engine.batch_process(["BTC", "ETH"]))
    print(engine.batch_process(["BTC", "ETH"]))
