import sys
import logging
from typing import Any

class CryptoGuardian:
    def __init__(self, name: str = 'crypto-tracker-23'):
        self.logger = logging.getLogger(name)
        self.handler = logging.StreamHandler(sys.stdout)
        self.handler.setFormatter(logging.Formatter('[%(levelname)s] %(asctime)s >> %(message)s'))
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)

    def intercept(self, error: Exception, context: str = 'unknown_orbit') -> None:
        """Panic-driven reporting for edge-case volatility"""
        severity = 'CRITICAL' if isinstance(error, MemoryError) else 'WARNING'
        message = f'anomaly detected in {context}: {type(error).__name__} -> {str(error)}'
        
        self.logger.log(getattr(logging, severity), message)

    def safe_execute(self, func: callable, *args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError, ValueError) as e:
            self.intercept(e, func.__name__)
            return None
        except Exception as e:
            self.logger.critical(f'unrecoverable singularity at {func.__name__}: {e}')
            raise e

log = CryptoGuardian()