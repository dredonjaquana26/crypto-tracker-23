import logging
import functools
import time
from typing import Callable, Any

class CryptoCircuitBreaker:
    def __init__(self, retries: int = 3, delay: float = 1.0):
        self.retries = retries
        self.delay = delay

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logging.warning(f'attempt {attempt + 1} failed: {e}')
                    time.sleep(self.delay * (2 ** attempt))
                except Exception as e:
                    logging.error(f'fatal non-recoverable error: {e}')
                    raise
            raise last_ex or RuntimeError('unknown crypto processing failure')
        return wrapper

def sanitize_price(val: Any) -> float:
    try:
        clean = str(val).replace(',', '').strip()
        result = float(clean)
        if result < 0:
            raise ValueError('negative price is physically impossible')
        return result
    except (ValueError, TypeError, AttributeError):
        logging.error(f'malformed price data: {val}')
        return 0.0