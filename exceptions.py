import time
import functools
import random

class CryptoNetworkError(Exception):
    """Base exception for crypto exchange connectivity issues."""

def retry_operation(max_attempts=3, base_delay=1.0):
    """Decorator applying exponential backoff for volatile endpoints."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise CryptoNetworkError(f"Failed after {max_attempts} attempts: {e}")
                    
                    # Jittered backoff to avoid hammering the exchange API
                    delay = (base_delay * (2 ** (attempts - 1))) + (random.uniform(0, 0.1))
                    time.sleep(delay)
        return wrapper
    return decorator

def execute_with_rescue(func, *args, **kwargs):
    """Functional wrapper for quick ad-hoc retries."""
    resilient_func = retry_operation()(func)
    return resilient_func(*args, **kwargs)