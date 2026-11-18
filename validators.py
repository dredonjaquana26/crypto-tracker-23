import time
import functools
import random
from typing import Callable, Any

def exponential_backoff(retries: int = 3, base_delay: float = 1.0):
    """Wrapper to dance with unstable crypto exchange APIs."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    # Jitter is the secret sauce for concurrent crypto requests
                    delay = (base_delay * (2 ** attempt)) + (random.random() * 0.5)
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@exponential_backoff(retries=5)
def fetch_market_price(ticker: str):
    """Sample operation prone to network volatility."""
    import requests
    response = requests.get(f"https://api.crypto.com/v1/price/{ticker}")
    response.raise_for_status()
    return response.json().get("price")