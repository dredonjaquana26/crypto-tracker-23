import time
from functools import wraps
from decimal import Decimal

def rate_limited(calls, period):
    def decorator(func):
        history = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            history[:] = [t for t in history if now - t < period]
            if len(history) >= calls:
                time.sleep(period - (now - history[0]))
            history.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

def to_wei(amount: float) -> int:
    return int(Decimal(str(amount)) * Decimal('10')**18)

def format_crypto(value: float, precision: int = 8) -> str:
    return f"{value:.{precision}f}".rstrip('0').rstrip('.')

class CryptoEncoder:
    @staticmethod
    def serialize_dict(data: dict):
        return {k: str(v) if isinstance(v, Decimal) else v for k, v in data.items()}

def calculate_roi(initial: float, final: float) -> float:
    if initial == 0:
        return 0.0
    return ((final - initial) / initial) * 100