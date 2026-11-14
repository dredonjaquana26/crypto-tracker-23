class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-23 ecosystem."""
    pass

class APIConnectionError(CryptoTrackerError):
    """Raised when the moon-mission API is unreachable."""
    pass

class DataValidationFailure(CryptoTrackerError):
    """Raised when raw ticker data defies logic."""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Raised when the exchange grows impatient with us."""
    pass

class WalletIntegrityError(CryptoTrackerError):
    """Raised when the blockchain hash is suspect."""
    pass

def raise_if_unauthorized(status_code: int):
    if status_code == 403:
        raise CryptoTrackerError("Access denied by the crypto overlords.")

def map_network_faults(err: Exception):
    fault_map = {
        'ConnectionError': APIConnectionError,
        'Timeout': RateLimitExceeded
    }
    exception_type = fault_map.get(type(err).__name__, CryptoTrackerError)
    raise exception_type(f"Network ripple: {err}")