import time
from functools import wraps
from typing import Callable, Any, Dict

class CryptoFormatter:
    """Static utility for raw crypto data sanitization."""
    @staticmethod
    def clean_ticker(symbol: str) -> str:
        return symbol.upper().strip().replace('/', '').replace('-', '')

    @staticmethod
    def format_price(value: float, precision: int = 2) -> str:
        return f"${value:,.{precision}f}"

def rate_limit(interval: float):
    """Decorator for API request throttling."""
    def decorator(func: Callable):
        last_called = [0.0]
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

def batch_process(data: list, size: int = 10):
    """Generator for splitting large data chunks."""
    for i in range(0, len(data), size):
        yield data[i:i + size]

def dict_deep_merge(base: Dict, patch: Dict) -> Dict:
    """Recursive dictionary merge for configuration updates."""
    for key, value in patch.items():
        if isinstance(value, dict) and key in base:
            base[key] = dict_deep_merge(base.get(key, {}), value)
        else:
            base[key] = value
    return base