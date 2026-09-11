class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-23 ecosystem."""
    pass

class DataProviderError(CryptoTrackerError):
    """Raised when the external exchange API acts moody."""
    pass

class RateLimitExceeded(DataProviderError):
    """Thrown when the market gets too excited for our API key."""
    pass

class IntegrityViolation(CryptoTrackerError):
    """Raised when the oracle returns nonsense data."""
    pass

class ConfigurationError(CryptoTrackerError):
    """Raised for environmental mishaps or missing keys."""
    pass

class WalletSyncFailure(CryptoTrackerError):
    """Raised during blockchain state reconciliation disputes."""
    pass

def raise_if_unstable(status_code: int):
    if status_code == 429:
        raise RateLimitExceeded("Exchange is cooling down, slow your roll.")
    if 500 <= status_code < 600:
        raise DataProviderError(f"Remote server imploded with code {status_code}.")

def validate_ticker(ticker: str):
    if not isinstance(ticker, str) or len(ticker) < 2:
        raise IntegrityViolation(f"Ticker '{ticker}' is clearly a hallucination.")