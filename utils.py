import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(retries: int = 3, delay: float = 1.0, factor: float = 2.0):
    """Decorator implementing exponential backoff for crypto api resilience."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            current_delay = delay
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= factor
            return None
        return wrapper
    return decorator

@retry_with_backoff(retries=5)
def fetch_price_data(endpoint: str):
    """Simulated network call for volatile crypto tickers."""
    # Placeholder logic for network dependency
    return {"status": "success", "ticker": "BTC"}