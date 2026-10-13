import time
from decimal import Decimal
from functools import wraps

def price_to_decimal(val):
    try:
        return Decimal(str(val))
    except (ValueError, TypeError):
        return Decimal('0.0')

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @wraps(func)
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

class CryptoTicker:
    def __init__(self, symbol, base_val='0'):
        self.symbol = symbol
        self.balance = price_to_decimal(base_val)

    def update_balance(self, amount):
        self.balance += price_to_decimal(amount)
        return self.balance

    def format_view(self):
        return f"[{self.symbol.upper()}]: {self.balance:,.8f}"

def sanitize_pair(pair):
    return pair.upper().replace('-', '/').strip()

if __name__ == '__main__':
    tracker = CryptoTicker('BTC', '0.005')
    print(tracker.format_view())