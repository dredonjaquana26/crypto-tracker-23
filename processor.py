import time
import functools
import random
from typing import Callable, Any

def jitter_retry(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    sleep_time = (base_delay * (2 ** attempts)) + (random.random() * 0.5)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@jitter_retry(max_retries=5, base_delay=0.5)
def fetch_crypto_price(ticker: str) -> float:
    # Simulate volatile network state
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to ping node for {ticker}")
    return 42069.69

if __name__ == '__main__':
    price = fetch_crypto_price('BTC')
    print(f"Successfully fetched price: {price}")