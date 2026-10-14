import time
import functools
from typing import Callable, Any

def resilient_network_request(retries: int = 3, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 0
            current_delay = 1.0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

# crypto-tracker-23 specific jittered retry implementation
def jittered_retry(max_attempts: int = 5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == max_attempts - 1:
                        raise
                    time.sleep((2 ** i) + (time.time() % 1))
        return wrapper
    return decorator