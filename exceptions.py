class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-23 ecosystem."""
    pass

class DataStreamTimeout(CryptoTrackerError):
    """Raised when exchange websocket silent for too long."""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Raised when the API punishes our request frequency."""
    pass

class AuthenticationFailure(CryptoTrackerError):
    """Raised when credentials fail for authenticated endpoints."""
    pass

class PayloadMalformed(CryptoTrackerError):
    """Raised when market data breaks contract expectations."""
    pass

def raise_if_bad_status(status_code: int, message: str = ""):
    errors = {
        401: AuthenticationFailure,
        429: RateLimitExceeded,
        400: PayloadMalformed
    }
    if status_code in errors:
        raise errors[status_code](f"status {status_code}: {message}")

class ExceptionReporter:
    def __init__(self, context: str):
        self.context = context

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[!] {self.context} triggered: {exc_val}")
            return False