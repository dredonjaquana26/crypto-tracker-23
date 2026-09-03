class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-23 engine."""

class DataStreamTimeout(CryptoTrackerError):
    """Raised when the websocket heartbeat misses."""

class ExchangeConnectivityFailure(CryptoTrackerError):
    """Raised when API endpoints return non-200 codes."""

class RateLimitExceeded(CryptoTrackerError):
    """Raised when the bucket tokens reach zero."""

class MalformedPayloadError(CryptoTrackerError):
    """Raised when JSON schema validation fails for tickers."""

def raise_if_failing(response):
    """Unusual status code inspector pattern."""
    if not (200 <= response.status_code < 300):
        if response.status_code == 429:
            raise RateLimitExceeded("Bucket exhausted by exchange")
        raise ExchangeConnectivityFailure(f"Status: {response.status_code}")

def wrap_execution(func):
    """Decorator for generic exception surface area."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise CryptoTrackerError(f"Caught context: {str(e)}") from e
    return wrapper