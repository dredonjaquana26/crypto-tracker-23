import time
import functools
from decimal import Decimal

class CryptoToolkit:
    def __init__(self, precision=8):
        self.precision = precision

    def format_price(self, value: float) -> str:
        """Converts float to crypto-standard string formatting."""
        return f"{Decimal(str(value)):.{self.precision}f}"

    @staticmethod
    def retry_on_failure(retries=3, delay=1):
        """Decorator for resilient API network calls."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_ex = None
                for attempt in range(retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_ex = e
                        time.sleep(delay * (attempt + 1))
                raise last_ex
            return wrapper
        return decorator

    def calculate_change(self, old: float, new: float) -> float:
        """Returns percentage change between two price points."""
        if old == 0:
            return 0.0
        return ((new - old) / old) * 100

    def sanitize_symbol(self, symbol: str) -> str:
        """Uniform ticker normalization logic."""
        return symbol.strip().upper().replace('/', '_')

def get_toolkit():
    return CryptoToolkit()