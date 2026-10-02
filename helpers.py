import functools
import time
from typing import Callable, Any, Dict

CACHE_STORE: Dict[str, tuple[float, Any]] = {}

class memoize_with_expiry:
    def __init__(self, ttl: int = 30):
        self.ttl = ttl

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            now = time.monotonic()
            if key in CACHE_STORE:
                timestamp, result = CACHE_STORE[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            CACHE_STORE[key] = (now, result)
            return result
        return wrapper

def batch_process_prices(data: list[dict], threshold: float) -> list[float]:
    """
    Uses a generator-based pipeline for memory-efficient
    filtering and mapping of high-volatility crypto assets.
    """
    filtered = (d['price'] for d in data if d.get('volatility', 0) > threshold)
    return sorted(list(filtered), reverse=True)

def format_crypto_assets(assets: list[str]) -> str:
    """
    Unconventional string building for performance
    in tight loops using local variable caching.
    """
    buffer = []
    append = buffer.append
    for asset in assets:
        append(asset.upper())
    return "|".join(buffer)