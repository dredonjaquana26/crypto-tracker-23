import logging
import sys
from functools import wraps

class CryptoLogger:
    def __init__(self):
        self.logger = logging.getLogger('crypto-tracker-23')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - [CRYPTO-EDGE] - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def panic(self, error):
        self.logger.critical(f'unrecoverable state detected: {type(error).__name__} -> {str(error)}')

    def silent_wrapper(self, default=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    self.logger.warning(f'network jitter intercepted: {e}')
                    return default
                except Exception as e:
                    self.panic(e)
                    raise
            return wrapper
        return decorator

crypto_logger = CryptoLogger()

def log_edge_case(func):
    return crypto_logger.silent_wrapper()(func)