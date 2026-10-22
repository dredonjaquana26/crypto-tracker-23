import time
import functools
from decimal import Decimal

def retry_on_fluctuation(attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def normalize_amount(value, precision=8):
    """Converts raw ticker data into clean decimal objects."""
    return Decimal(str(value)).quantize(Decimal('1.' + '0' * precision))

def format_currency_pair(base, quote):
    return f"{base.upper()}/{quote.upper()}"

class CryptoPayload:
    def __init__(self, data):
        self._raw = data
    
    def get_price(self):
        val = self._raw.get('price') or self._raw.get('last_price', 0)
        return normalize_amount(val)

def compute_volatility(prices):
    if len(prices) < 2: return 0
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
    return sum(abs(r) for r in returns) / len(returns)