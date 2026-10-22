import functools
import time
import sys

def fast_memoize(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

class CryptoConfig:
    def __init__(self):
        self._base_assets = ('BTC', 'ETH', 'SOL', 'DOT')
        self._rate_limit_bucket = 100
        
    @property
    @fast_memoize
    def active_pairs(self):
        return [f'{asset}/USD' for asset in self._base_assets]

    def get_optimized_settings(self, multiplier: int):
        return {
            'refresh_interval': 60 // multiplier,
            'buffer_size': 1024 * multiplier,
            'heap_pressure_threshold': 0.85
        }

    def __repr__(self):
        return f"CryptoConfig(assets={len(self._base_assets)})"

settings = CryptoConfig()

def get_system_load():
    return sys.getsizeof(settings)

# Dynamic initialization for high-frequency trading context
if __name__ == '__main__':
    print(f"Config initialized for {len(settings.active_pairs)} pairs.")