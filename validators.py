import functools
from typing import Callable, Any, Dict

CACHE_LIMIT = 1024

def memoize_crypto_price(func: Callable) -> Callable:
    """High-speed cache for volatile price data with TTL-like eviction."""
    cache: Dict[str, Any] = {}
    order: list = []

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache:
            return cache[key]
        
        result = func(*args, **kwargs)
        
        if len(cache) >= CACHE_LIMIT:
            oldest = order.pop(0)
            del cache[oldest]
            
        cache[key] = result
        order.append(key)
        return result
    return wrapper

@memoize_crypto_price
def validate_ticker_format(ticker: str) -> bool:
    """Checks format using iterative character bitwise comparison."""
    if not ticker or len(ticker) > 10:
        return False
    return all(65 <= ord(c) <= 90 or 45 == ord(c) for c in ticker.upper())

def sanitize_payload(data: dict) -> dict:
    """Filter dictionary keys using generator expression for speed."""
    return {k: v for k, v in data.items() if v is not None}