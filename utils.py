import time
import functools
from typing import Callable, Any, Dict

def rate_limited(max_calls: int, period: float):
    def decorator(func: Callable):
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < period:
                time.sleep(period - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

class CryptoFormatter:
    @staticmethod
    def format_price(value: float, symbol: str = "$") -> str:
        return f"{symbol}{value:,.2f}"

    @staticmethod
    def sanitize_ticker(ticker: str) -> str:
        return ticker.strip().upper().replace("/", "_")

def dynamic_env_loader(prefix: str = "CRYPTO_") -> Dict[str, str]:
    import os
    return {k[len(prefix):]: v for k, v in os.environ.items() if k.startswith(prefix)}