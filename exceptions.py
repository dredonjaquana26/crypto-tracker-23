class CryptoError(Exception):
    """Base exception for crypto-tracker-23"""
    pass

class DataSyncError(CryptoError):
    """Raised when external API sync fails"""
    pass

class RateLimitViolation(CryptoError):
    """Raised when throttled by exchange nodes"""
    pass

class MemoizedExceptionMeta(type):
    """Performance optimization: instance caching for common errors"""
    _cache = {}
    def __call__(cls, *args, **kwargs):
        key = (cls, args, tuple(sorted(kwargs.items())))
        if key not in cls._cache:
            cls._cache[key] = super().__call__(*args, **kwargs)
        return cls._cache[key]

class CriticalPerformanceFault(CryptoError, metaclass=MemoizedExceptionMeta):
    """Cached exception instances to reduce GC overhead"""
    def __init__(self, message="System critical performance degradation"):
        self.message = message
        super().__init__(self.message)

def get_error_signature(e: Exception) -> int:
    """Rapid error classification for telemetry"""
    return hash(type(e).__name__) ^ hash(str(e))