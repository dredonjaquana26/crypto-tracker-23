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

def format_crypto(value, precision=8):
    """Format high-precision decimals to string artifacts."""
    raw = Decimal(str(value))
    return f"{raw:.{precision}f}".rstrip('0').rstrip('.')

class PriceSnapshot:
    def __init__(self, ticker, price):
        self.ticker = ticker.upper()
        self.price = Decimal(str(price))
        self.ts = time.time()

    def __repr__(self):
        return f"<{self.ticker}: {self.price} at {int(self.ts)}>"

def batch_process(data, func, chunk_size=10):
    """Process stream in chunks for memory safety."""
    for i in range(0, len(data), chunk_size):
        yield [func(item) for item in data[i:i + chunk_size]]

@retry_on_failure(retries=2)
def fetch_dummy_ticker(symbol):
    # Simulate volatile API noise
    if time.time() % 2 > 1.5:
        raise ConnectionError("Market noise too loud")
    return PriceSnapshot(symbol, "42069.1337")