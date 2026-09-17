class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-23 ecosystem."""
    pass

class ExchangeRateError(CryptoTrackerError):
    """Raised when the oracle fails to fetch price data."""
    pass

class WalletBalanceError(CryptoTrackerError):
    """Raised during inconsistencies in ledger summation."""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Exponential backoff trigger for api throttling."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Cooldown active for {retry_after} seconds")

class DataIntegrityError(CryptoTrackerError):
    """Custom fault for corrupted transmission payloads."""
    pass

def raise_if_unstable(condition: bool, msg: str) -> None:
    if condition:
        raise CryptoTrackerError(f"Unstable state detected: {msg}")

class ExceptionDecorator:
    """Meta-wrapper for logging exotic failure modes."""
    @staticmethod
    def intercept(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[!] {func.__name__} crashed with: {e}")
                raise
        return wrapper