import time
import functools
import random

def retry_network_ops(retries=3, backoff=0.5):
    """Exponential backoff decorator for unstable crypto exchange APIs."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    sleep_time = (backoff * (2 ** attempt)) + (random.random() * 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def fetch_with_jitter(operation):
    """Functional wrapper for single-use network retry operations."""
    def execute(*args, **kwargs):
        for i in range(5):
            try:
                return operation(*args, **kwargs)
            except Exception:
                if i == 4: raise
                time.sleep(1 + i * 0.5)
    return execute