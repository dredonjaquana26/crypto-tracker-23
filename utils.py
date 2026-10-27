import time
import functools
from typing import Callable, Any

def rate_limited(max_per_second: int) -> Callable:
    min_interval = 1.0 / float(max_per_second)
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            elapsed = time.perf_counter() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.perf_counter()
            return ret
        return wrapper
    return decorator

def safe_crypto_cast(value: Any, default: float = 0.0) -> float:
    try:
        return float(str(value).replace(',', ''))
    except (ValueError, TypeError):
        return default

def memoize_crypto_price(ttl_seconds: int = 60) -> Callable:
    cache = {}
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args) -> Any:
            key = str(args)
            now = time.time()
            if key in cache and (now - cache[key]['ts']) < ttl_seconds:
                return cache[key]['val']
            res = func(*args)
            cache[key] = {'val': res, 'ts': now}
            return res
        return wrapper
    return decorator