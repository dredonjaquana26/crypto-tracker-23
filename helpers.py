import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=1.5):
    def decorator(func):
        @functools.wraps(func)
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

def to_decimal(val):
    return Decimal(str(val)).normalize()

def format_crypto_pair(base, quote):
    return f"{base.upper()}/{quote.upper()}"

def calculate_pct_change(old, new):
    old, new = Decimal(str(old)), Decimal(str(new))
    if old == 0:
        return Decimal('0')
    return ((new - old) / old) * 100

class CryptoFilter:
    def __init__(self, threshold):
        self.threshold = Decimal(str(threshold))

    def is_significant(self, value):
        return abs(Decimal(str(value))) >= self.threshold