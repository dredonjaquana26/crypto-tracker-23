import time
import functools
import random
from typing import Callable, Any

def retry_with_backoff(retries: int = 3, backoff_in_seconds: int = 1):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            x, v = 0, backoff_in_seconds
            while x < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    x += 1
                    if x == retries:
                        raise e
                    sleep_time = (v * (2 ** (x - 1))) + (random.randint(0, 1000) / 1000)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@retry_with_backoff(retries=5)
def fetch_crypto_data(url: str):
    import requests
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()