import time
import functools
from decimal import Decimal

def rate_limited(calls, period):
    def decorator(func):
        history = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            history[:] = [t for t in history if now - t < period]
            if len(history) >= calls:
                raise RuntimeError('Rate limit exceeded for crypto API')
            history.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def format_crypto_val(value: float, precision: int = 8) -> str:
    return f'{Decimal(str(value)):.{precision}f}'.rstrip('0').rstrip('.')

def deep_get(data: dict, path: str, default=None):
    keys = path.split('.')
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError):
            return default
    return data

def calculate_roi(initial: float, current: float) -> float:
    if initial == 0:
        return 0.0
    return ((current - initial) / initial) * 100