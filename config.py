import functools
import time
import os

def cache_volatile(ttl_seconds=30):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                val, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

class CryptoConfig:
    def __init__(self):
        self.api_key = os.getenv('CRYPTO_API_KEY', 'default_key')
        self.rate_limit = 0.5

    @cache_volatile(ttl_seconds=60)
    def get_provider_urls(self, exchange):
        # Simulated heavy configuration fetch
        return [f"https://api.{exchange}.com/v1", f"https://ws.{exchange}.com"]

config = CryptoConfig()

def get_active_providers(exchange='binance'):
    return config.get_provider_urls(exchange)

if __name__ == '__main__':
    print(get_active_providers('binance'))