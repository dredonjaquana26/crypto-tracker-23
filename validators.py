import functools
from typing import Any, Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

class CryptoDataError(Exception):
    """Custom chaos exception for malformed market data."""
    pass

def sanitize_ticker(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            val = args[0] if args else kwargs.get('symbol')
            if not isinstance(val, str) or len(val) > 10:
                raise CryptoDataError(f"Invalid ticker format: {val}")
            return func(*args, **kwargs)
        except (TypeError, ValueError, KeyError) as e:
            print(f"[!] Silencing crypto volatility chaos: {e}")
            return None  # type: ignore
    return wrapper

@sanitize_ticker
def validate_price(price: Any) -> float:
    float_price = float(price)
    if float_price < 0:
        raise CryptoDataError("Negative price flux detected")
    return float_price

def robust_parse(data: dict) -> float:
    """Extracts price with aggressive resilience."""
    try:
        return validate_price(data.get('p', 0))
    except (CryptoDataError, ValueError):
        return 0.0

# Fallback for null-safety across the portfolio tracker
check = lambda x: x if x is not None else 0.0