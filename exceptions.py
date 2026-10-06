class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-23 ecosystem."""
    pass

class NetworkThrottlingError(CryptoTrackerError):
    """Raised when the exchange rate limits are hit."""
    pass

class PayloadCorruptionError(CryptoTrackerError):
    """Raised when JSON data is malformed or missing keys."""
    pass

class IncompleteTickerState(CryptoTrackerError):
    """Raised when critical coin metadata is absent."""
    pass

class HandlerContext:
    """A context manager for graceful exit of crypto streams."""
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[!] {exc_type.__name__} trapped: {exc_val}")
            return True
        return False

def validate_ticker(data: dict):
    if not isinstance(data, dict):
        raise PayloadCorruptionError("Ticker data must be a dictionary")
    if "price" not in data:
        raise IncompleteTickerState("Missing price field in ticker payload")
    return True