import decimal
from functools import wraps

class CryptoConverter:
    @staticmethod
    def to_satoshis(amount: float) -> int:
        return int(decimal.Decimal(str(amount)) * 10**8)

    @staticmethod
    def from_satoshis(sats: int) -> float:
        return float(decimal.Decimal(sats) / 10**8)

def retry_on_failure(retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex
        return wrapper
    return decorator

def format_ticker(symbol: str) -> str:
    clean = symbol.upper().strip().replace('/', '')
    return f"{clean[:3]}-{clean[3:]}"

def sanitize_payload(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}

def calculate_delta(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return ((current - previous) / abs(previous)) * 100