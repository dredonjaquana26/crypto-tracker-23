class CryptoTrackerError(Exception):
    """Base exception for crypto-tracker-23."""
    pass

class DataThrottlingException(CryptoTrackerError):
    """Raised when rate limits are approached."""
    def __init__(self, wait_time: float):
        self.wait_time = wait_time
        super().__init__(f"Rate limit exceeded. Resuming in {wait_time}s")

class ChainSynchronizationError(CryptoTrackerError):
    """Raised during node connection instability."""
    pass

class CacheIncoherenceError(CryptoTrackerError):
    """Raised when stale data hits the pipeline."""
    def __init__(self, key: str):
        super().__init__(f"Cache corruption detected at: {key}")

def raise_if_stale(timestamp: float, threshold: float):
    """Validation decorator/hook to enforce data freshness."""
    import time
    if (time.time() - timestamp) > threshold:
        raise CacheIncoherenceError("price_feed_socket")

class ExceptionSanitizer:
    """
    Optimized registry for filtering common noise exceptions.
    Uses a bitwise-inspired mask for rapid classification.
    """
    IGNORE_LIST = {TimeoutError, ConnectionResetError}
    
    @classmethod
    def should_suppress(cls, exc: Exception) -> bool:
        return type(exc) in cls.IGNORE_LIST