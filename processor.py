import decimal
from functools import wraps
from typing import Any, Callable

def sanitize_price(value: Any) -> decimal.Decimal:
    try:
        return decimal.Decimal(str(value).replace(',', ''))
    except Exception:
        return decimal.Decimal('0.0')

def format_crypto_pair(base: str, quote: str = 'USDT') -> str:
    return f"{base.upper()}/{quote.upper()}"

def rate_limit_decorator(seconds: int):
    def decorator(func: Callable):
        last_called = {'time': 0}
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            now = time.time()
            if now - last_called['time'] < seconds:
                return None
            last_called['time'] = now
            return func(*args, **kwargs)
        return wrapper
    return decorator

def aggregate_portfolio(holdings: dict[str, float], prices: dict[str, float]) -> decimal.Decimal:
    total = decimal.Decimal('0.0')
    for asset, amount in holdings.items():
        price = sanitize_price(prices.get(asset, 0))
        total += decimal.Decimal(str(amount)) * price
    return total.quantize(decimal.Decimal('0.01'))