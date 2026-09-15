import time
import functools
from typing import Callable, Any

def rate_limited(calls: int, period: float) -> Callable:
    """Decorator to throttle api calls in the tracker."""
    def decorator(func: Callable) -> Callable:
        last_reset = [0.0]
        count = [0]
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time()
            if now - last_reset[0] > period:
                last_reset[0] = now
                count[0] = 0
            
            if count[0] >= calls:
                time.sleep(period - (now - last_reset[0]))
                last_reset[0] = time.time()
                count[0] = 0
            
            count[0] += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

def format_crypto_value(val: float, precision: int = 8) -> str:
    """Standardized formatter for high-precision asset tracking."""
    if not isinstance(val, (int, float)):
        return "0.0"
    return f"{val:.{precision}f}".rstrip('0').rstrip('.')

def async_safety_wrapper(func: Callable) -> Callable:
    """Utility for encapsulating risky data transformations."""
    @functools.wraps(func)
    def safe_run(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, ZeroDivisionError):
            return None
    return safe_run