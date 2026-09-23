import time
import functools
from typing import Callable, Any

def rate_limiter(calls: int, period: float):
    def decorator(func: Callable):
        state = {'count': 0, 'last_reset': time.time()}
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            now = time.time()
            if now - state['last_reset'] > period:
                state['count'] = 0
                state['last_reset'] = now
            if state['count'] >= calls:
                raise RuntimeError('Rate limit exceeded for crypto endpoint')
            state['count'] += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

def format_crypto_price(price: float, symbol: str) -> str:
    return f'{symbol.upper()}: ${price:,.2f}'

def sanitize_ticker(ticker: str) -> str:
    return ''.join(c for c in ticker if c.isalnum()).upper()

class CryptoPayloadEncoder:
    @staticmethod
    def transform(data: dict) -> dict:
        return {k.lower(): v for k, v in data.items() if v is not None}