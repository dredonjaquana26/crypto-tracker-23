import time
import random
import functools
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = base_delay * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_operation(max_attempts=4, base_delay=0.5)
def fetch_crypto_price(ticker: str) -> float:
    # simulate volatile api access
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach market for {ticker}")
    return round(random.uniform(1000.0, 60000.0), 2)

if __name__ == "__main__":
    price = fetch_crypto_price("BTC")
    print(f"Current price: ${price}")