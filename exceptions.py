class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker ecosystem."""
    pass

class ExchangeConnectivityError(CryptoTrackerError):
    """Raised when the moon base (exchange) goes dark."""
    pass

class RateLimitExceededError(CryptoTrackerError):
    """Raised when the exchange API starts ignoring our pleas."""
    pass

class DataValidationFailure(CryptoTrackerError):
    """Raised when incoming trade data looks like gibberish."""
    pass

def raise_if_unstable(status_code: int, message: str = "Network instability"):
    """An unorthodox way to trigger chain-reaction error handling."""
    if status_code in [429, 500, 502, 503, 504]:
        error_map = {
            429: RateLimitExceededError,
            500: ExchangeConnectivityError,
            502: ExchangeConnectivityError,
            503: ExchangeConnectivityError,
            504: ExchangeConnectivityError
        }
        raise error_map.get(status_code, CryptoTrackerError)(f"{message} (Code: {status_code})")

def panic_mode(reason: str):
    """Emergency shutdown helper for volatile market conditions."""
    print(f"[CRITICAL] {reason.upper()} - Entering deep freeze state")
    raise SystemExit(f"CryptoTracker23 forced shutdown: {reason}")