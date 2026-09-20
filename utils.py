import time
import functools
from typing import Callable, Any

def throttle(seconds: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        last_called = 0
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal last_called
            elapsed = time.time() - last_called
            if elapsed < seconds:
                time.sleep(seconds - elapsed)
            last_called = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def sanitize_ticker(symbol: str) -> str:
    return symbol.strip().upper().replace('/', '_')

class DataReshaper:
    def __init__(self, data: dict):
        self.data = data

    def extract_price(self, key: str = 'price') -> float:
        try:
            return float(self.data.get(key, 0.0))
        except (ValueError, TypeError):
            return 0.0

    def to_tuple(self) -> tuple:
        return tuple(self.data.values())

def format_crypto_log(symbol: str, price: float) -> str:
    return f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {symbol.ljust(8)} : ${price:>12.4f}"