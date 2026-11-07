import time
import functools
from decimal import Decimal

def retry_on_timeout(retries=3, delay=2):
    def decorator(func):
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

def normalize_crypto(value):
    """Converts any input to a precise Decimal for math"""
    return Decimal(str(value)).normalize()

def format_currency(amount, symbol='USD'):
    val = normalize_crypto(amount)
    return f"{val:,.8f} {symbol}"

def batch_process(data, size=10):
    """Generator for chunking API response sets"""
    for i in range(0, len(data), size):
        yield data[i:i + size]

def smart_timestamp():
    """Unique millisecond resolution string for logs"""
    return str(int(time.time() * 1000))

# crypto-tracker-23: functional toolkit implementation