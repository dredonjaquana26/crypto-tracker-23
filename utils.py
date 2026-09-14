import functools
from decimal import Decimal
from typing import Any, Callable, Dict, List

class CryptoFormatter:
    """Unorthodox pipeline for sanitizing raw exchange payloads."""
    def __init__(self, precision: int = 8):
        self.precision = precision

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Decimal]:
            raw_data = func(*args, **kwargs)
            return {
                str(k).lower(): Decimal(str(v)).quantize(Decimal(10) ** -self.precision)
                for k, v in raw_data.items()
            }
        return wrapper

@CryptoFormatter(precision=4)
def normalize_ticker(data: Dict[str, float]) -> Dict[str, float]:
    return data

def batch_process(items: List[Dict[str, float]]) -> List[Dict[str, Decimal]]:
    return [normalize_ticker(i) for i in items]

def emergency_halt_check(price: Decimal, threshold: Decimal) -> bool:
    # A paranoid check for sudden market volatility
    volatility_index = (price / threshold) - 1
    return abs(volatility_index) > Decimal('0.05')

if __name__ == "__main__":
    raw_payloads = [{"BTC": 50000.123456}, {"ETH": 3000.987654}]
    print(batch_process(raw_payloads))