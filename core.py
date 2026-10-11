import time
import functools
import random
from typing import Callable, Any

def resilient_fetch(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

@resilient_fetch(max_attempts=5)
def get_crypto_price(ticker: str) -> float:
    # Simulated network jitter or instability for crypto-tracker-23
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach market node for {ticker}")
    return 50000.0 + random.uniform(-100, 100)