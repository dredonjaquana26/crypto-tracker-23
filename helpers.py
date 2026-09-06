import time
import functools
from typing import Callable, Any

def rate_limited(calls: int, period: float) -> Callable:
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < period:
                time.sleep(period - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

def format_crypto_amount(amount: float, symbol: str = 'BTC') -> str:
    precision = 8 if symbol == 'BTC' else 4
    return f"{amount:.{precision}f} {symbol}"

class CryptoDataSanitizer:
    def __init__(self, raw_data: dict):
        self.data = raw_data

    def sanitize(self) -> dict:
        return {
            k.lower().strip(): float(v) 
            for k, v in self.data.items() 
            if v is not None
        }

def retry_on_failure(retries: int = 3, delay: int = 1):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == retries - 1: raise
                    time.sleep(delay)
        return wrapper
    return decorator