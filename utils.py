import time
from functools import wraps
from typing import Callable, Any

def retry_strategy(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def sanitize_ticker(symbol: str) -> str:
    return str(symbol).strip().upper().replace('/', '_')

class CryptoFormatter:
    @staticmethod
    def format_currency(amount: float, pair: str = 'USD') -> str:
        return f"{amount:,.2f} {pair}"

def batch_process(data: list, size: int = 10):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def timestamp_now() -> int:
    return int(time.time())