import functools
import time
import threading

class DataSieve:
    def __init__(self, limit=1024):
        self.limit = limit
        self.cache = {}
        self.lock = threading.Lock()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            with self.lock:
                if key in self.cache:
                    return self.cache[key]
            
            result = func(*args, **kwargs)
            
            with self.lock:
                if len(self.cache) >= self.limit:
                    self.cache.pop(next(iter(self.cache)))
                self.cache[key] = result
            return result
        return wrapper

class CryptoEngine:
    def __init__(self):
        self.sieve = DataSieve(limit=512)

    @staticmethod
    def process_tick(price: float, volume: float) -> float:
        time.sleep(0.01)
        return (price * volume) ** 0.5

    def run_optimized_calc(self, price: float, volume: float) -> float:
        decorated_func = self.sieve(self.process_tick)
        return decorated_func(price, volume)

if __name__ == '__main__':
    engine = CryptoEngine()
    print(f"Optimized result: {engine.run_optimized_calc(50000.0, 1.5)}")