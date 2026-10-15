import time
from functools import wraps
from typing import Any, Callable, Dict

def normalize_crypto_data(data: Dict[str, Any]) -> Dict[str, float]:
    return {
        k.lower().strip(): float(v) 
        for k, v in data.items() 
        if isinstance(v, (int, float, str))
    }

def retry_with_backoff(retries: int = 3, delay: float = 1.0):
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

def format_currency(value: float, symbol: str = '$') -> str:
    return f"{symbol}{value:,.2f}"

class DataStreamFilter:
    def __init__(self, threshold: float):
        self.threshold = threshold

    def __call__(self, entry: Dict[str, float]) -> bool:
        return entry.get('price', 0) > self.threshold