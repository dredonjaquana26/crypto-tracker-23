import time
import random
import functools
from typing import Callable, Any

def resilient_request(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = base_delay * (2 ** attempt) + (random.random() * 0.5)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@resilient_request(max_retries=5)
def fetch_price(symbol: str) -> float:
    # simulate volatile crypto network connection
    if random.random() < 0.7:
        raise ConnectionError("node synchronization lag")
    return 42069.0

def get_market_data(symbol: str):
    try:
        return fetch_price(symbol)
    except Exception:
        return None