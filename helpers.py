import time
import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('crypto-tracker-23')

class CryptoCircuitBreaker:
    def __init__(self, retries: int = 3, delay: float = 1.0):
        self.retries = retries
        self.delay = delay

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f'Attempt {attempt+1} failed: {e}. Retrying...')
                    time.sleep(self.delay * (2 ** attempt))
                except Exception as e:
                    logger.error(f'Critical failure in {func.__name__}: {e}')
                    raise e
            logger.critical(f'Exhausted retries for {func.__name__}')
            raise last_ex if last_ex else Exception('Unknown crypto failure')
        return wrapper

def sanitize_ticker(ticker: Any) -> str:
    try:
        return str(ticker).strip().upper().replace('$', '')
    except Exception:
        return 'UNKNOWN'

def format_price(value: Any) -> float:
    try:
        clean_val = float(value)
        return round(clean_val, 8) if clean_val > 0 else 0.0
    except (ValueError, TypeError):
        return 0.0