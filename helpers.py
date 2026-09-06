import math
from typing import Callable, Any, Dict, List

class RecoveryRegistry:
    """Registry for fallback strategies when crypto calculations fail."""
    def __init__(self):
        self.history: List[float] = [1.0]

    def record(self, val: float) -> float:
        if not math.isnan(val) and not math.isinf(val):
            self.history.append(val)
            if len(self.history) > 10:
                self.history.pop(0)
        return val

    def get_fallback(self) -> float:
        return sum(self.history) / len(self.history)

recovery = RecoveryRegistry()

def resilient_crypto_calc(default_on_fail: Any = None) -> Callable:
    """Decorator to handle edge cases like ZeroDivision or NaN in volatile calculations."""
    def decorator(func: Callable[..., float]) -> Callable[..., float]:
        def wrapper(*args: Any, **kwargs: Any) -> float:
            try:
                result = func(*args, **kwargs)
                if math.isnan(result) or math.isinf(result):
                    raise ValueError("Invalid numerical result (NaN/Inf)")
                return recovery.record(result)
            except (ZeroDivisionError, TypeError, ValueError):
                fallback = recovery.get_fallback() if default_on_fail is None else default_on_fail
                return fallback
        return wrapper
    return decorator

@resilient_crypto_calc()
def calculate_price_impact(volume: float, liquidity: float) -> float:
    """Calculates price impact, highly prone to ZeroDivisionError in low liquidity pools."""
    return volume / liquidity

@resilient_crypto_calc(default_on_fail=0.0)
def calculate_volatility_index(prices: List[float]) -> float:
    """Calculates volatility, prone to ValueError with empty or single-element lists."""
    mean = sum(prices) / len(prices)
    variance = sum((x - mean) ** 2 for x in prices) / (len(prices) - 1)
    return math.sqrt(variance)