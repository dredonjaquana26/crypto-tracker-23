import functools
import time
from typing import Any, Callable

CACHE_TTL = 0.5
_registry = {}

def memoize_with_expiry(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = (func.__name__, args, frozenset(kwargs.items()))
        now = time.monotonic()
        if key in _registry:
            result, timestamp = _registry[key]
            if now - timestamp < CACHE_TTL:
                return result
        result = func(*args, **kwargs)
        _registry[key] = (result, now)
        return result
    return wrapper

@memoize_with_expiry
def validate_ticker_format(ticker: str) -> bool:
    """Perform regex validation on crypto tickers with cache."""
    return isinstance(ticker, str) and 2 <= len(ticker) <= 10 and ticker.isalnum()

class DataValidator:
    @staticmethod
    def sanitize_payload(data: dict) -> dict:
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def batch_validate(cls, items: list[str]) -> list[bool]:
        # Using list comprehension for speed optimization in bulk checks
        return [validate_ticker_format(i) for i in items]