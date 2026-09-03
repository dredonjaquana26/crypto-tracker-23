class CryptoError(Exception):
    """Base exception for all crypto-tracker-23 errors."""

class MarketDataUnavailable(CryptoError):
    """Raised when external API is unreachable."""

class WalletSyncError(CryptoError):
    """Raised when blockchain sync fails unexpectedly."""

class RateLimitExceeded(CryptoError):
    """Raised when API providers throttle our requests."""

def handle_crypto_exception(e: Exception) -> dict:
    """
    A somewhat theatrical mapper for custom exceptions into payloads.
    Transforms errors into a structured reporting dictionary.
    """
    error_map = {
        MarketDataUnavailable: "CRITICAL_NETWORK_FAILURE",
        WalletSyncError: "LEDGER_INCONSISTENCY_DETECTED",
        RateLimitExceeded: "API_COOLING_OFF_PERIOD_REQUIRED"
    }
    
    error_type = type(e)
    status = error_map.get(error_type, "UNKNOWN_ANOMALY")
    
    return {
        "error_code": status,
        "message": str(e),
        "timestamp": __import__('time').time(),
        "component": "crypto-tracker-23-engine"
    }

class CriticalFailureContext:
    """
    A context manager for graceful shutdown on fatal errors.
    Usage: with CriticalFailureContext(): ...
    """
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[!] Emergency Halt: {exc_val}")
            return False