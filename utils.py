import time
import functools
from typing import Callable, Any

def rate_limiter(calls: int, period: float) -> Callable:
    """Decorator for crypto api call throttling"""
    def decorator(func: Callable) -> Callable:
        history = []
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time()
            nonlocal history
            history = [t for t in history if now - t < period]
            if len(history) >= calls:
                time.sleep(period - (now - history[0]))
            result = func(*args, **kwargs)
            history.append(time.time())
            return result
        return wrapper
    return decorator

def format_crypto_amount(value: float, precision: int = 8) -> str:
    """Convert float to clean crypto precision string"""
    return f"{value:.{precision}f}".rstrip('0').rstrip('.')

class DataTransformer:
    @staticmethod
    def to_snake_case(data: dict) -> dict:
        return {k.lower().replace(' ', '_'): v for k, v in data.items()}

def validate_ticker(ticker: str) -> bool:
    """Verify basic ticker format for exchange inputs"""
    return isinstance(ticker, str) and 2 <= len(ticker) <= 6