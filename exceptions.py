class CryptoTrackerError(Exception):
    """Base exception for crypto-tracker-23"""
    pass

class ExchangeConnectionError(CryptoTrackerError):
    """Raised when the socket goes rogue"""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Raised when the exchange tells us to chill"""
    pass

class DataParsingError(CryptoTrackerError):
    """Raised when the API returns gibberish"""
    pass

def handle_crypto_exception(func):
    """Decorator for wrapping operations in cosmic silence"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CryptoTrackerError as e:
            print(f"[!] {type(e).__name__} caught: {e}")
            return None
        except Exception as e:
            print(f"[!] Unhandled anomaly: {e}")
            raise e
    return wrapper

class CustomExceptionFactory:
    """Dynamic generation of granular error types"""
    @staticmethod
    def create(name: str):
        return type(name, (CryptoTrackerError,), {})

API_LIMIT_EXCEEDED = CustomExceptionFactory.create('APILimitExceeded')