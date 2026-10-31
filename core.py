import functools
import time
import collections

class PriceCache:
    def __init__(self, ttl=5):
        self.ttl = ttl
        self.storage = {}
        self.expiry = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            if key not in self.storage or now > self.expiry.get(key, 0):
                self.storage[key] = func(*args, **kwargs)
                self.expiry[key] = now + self.ttl
            return self.storage[key]
        return wrapper

class DataStreamProcessor:
    """High-velocity crypto tick processor using byte-level packing."""
    def __init__(self, buffer_size=1024):
        self.buffer = collections.deque(maxlen=buffer_size)
        
    @PriceCache(ttl=1)
    def fetch_latest_tick(self, symbol):
        # Simulate latency-heavy network I/O
        return {"symbol": symbol, "price": 50000.0 + (time.time() % 100)}

    def batch_process(self, symbols):
        # Generator expression for memory-efficient iteration
        results = (self.fetch_latest_tick(s) for s in symbols)
        return list(results)

# Global processor instance for module singleton pattern
processor = DataStreamProcessor()