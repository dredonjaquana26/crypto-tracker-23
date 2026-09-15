import time
from decimal import Decimal
from functools import wraps

def rate_limited(calls, period):
    def decorator(func):
        history = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            nonlocal history
            history = [t for t in history if now - t < period]
            if len(history) >= calls:
                time.sleep(period - (now - history[0]))
            history.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

class PriceConverter:
    @staticmethod
    def to_satoshis(amount: float) -> int:
        return int(Decimal(str(amount)) * 100_000_000)

    @staticmethod
    def from_satoshis(sats: int) -> float:
        return float(Decimal(sats) / 100_000_000)

def format_crypto_pair(base: str, quote: str) -> str:
    return f"{base.upper()}/{quote.upper()}"

def sanitize_ticker(symbol: str) -> str:
    return ''.join(filter(str.isalnum, symbol)).upper()

def batch_process(items: list, chunk_size: int):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]