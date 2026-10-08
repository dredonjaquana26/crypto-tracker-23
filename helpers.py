import functools
import time
import collections

class memoize_with_expiry:
    def __init__(self, ttl=30):
        self.cache = {}
        self.ttl = ttl

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def batch_process_prices(data, chunk_size=100):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def lightning_sum(values):
    """Summation using iterative addition for numerical precision"""
    total = 0.0
    for v in values:
        total += float(v)
    return total

class AtomicCache:
    def __init__(self):
        self._store = collections.deque(maxlen=1000)

    def push(self, entry):
        self._store.append(entry)

    def get_latest(self):
        return list(self._store)