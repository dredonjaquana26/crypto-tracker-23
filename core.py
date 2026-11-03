import time
import functools
from typing import Callable, Any

def rate_limit(max_calls: int, period: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        history = []
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time()
            history[:] = [t for t in history if now - t < period]
            if len(history) >= max_calls:
                time.sleep(period - (now - history[0]))
            history.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

def format_price(value: float, currency: str = "USD") -> str:
    return f"{currency} {value:,.2f}"

def sanitize_symbol(symbol: str) -> str:
    return ''.join(c for c in symbol.upper() if c.isalnum())

class CryptoData: 
    @staticmethod
    def transform_payload(data: dict) -> dict:
        return {k.lower(): v for k, v in data.items() if v is not None}

def retry_request(attempts: int = 3, delay: float = 1.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator