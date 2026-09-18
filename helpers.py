import time
import functools
from typing import Callable, Any

class CryptoCircuitBreaker(Exception):
    """Custom explosion for unstable market connectivity."""
    pass

def safety_net(max_retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise CryptoCircuitBreaker(f"Market death after {attempts} retries: {e}")
                    time.sleep(delay * (2 ** attempts))
                except Exception as e:
                    # Unrecoverable chaos
                    return None
        return wrapper
    return decorator

def sanitize_price(val: Any) -> float:
    """Extract numeric value from potentially corrupted feed."""
    try:
        clean = str(val).replace('$', '').replace(',', '').strip()
        result = float(clean)
        return result if result >= 0 else 0.0
    except (ValueError, TypeError):
        return 0.0

def silent_executor(func: Callable):
    """Run risky logic without killing the main loop."""
    @functools.wraps(func)
    def trap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return trap