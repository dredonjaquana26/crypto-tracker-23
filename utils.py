import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger('crypto-tracker-23')

class CryptoCircuitBreaker:
    def __init__(self, retries: int = 3):
        self.retries = retries

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except ConnectionError as e:
                    attempts += 1
                    logger.warning(f"network instability detected: {e}")
                    if attempts == self.retries:
                        raise ConnectionError("max retries reached for provider")
                except Exception as e:
                    logger.error(f"catastrophic failure in {func.__name__}: {str(e)}")
                    return None
        return wrapper

def safe_request(func: Callable) -> Callable:
    @wraps(func)
    def packet_check(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return {'status': 'err', 'payload': {}}
        return {'status': 'ok', 'data': result}
    return packet_check