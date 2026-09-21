from typing import Optional, Any

class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-23 ecosystem."""
    def __init__(self, message: str, payload: Optional[Any] = None) -> None:
        super().__init__(message)
        self.payload = payload

class RateLimitExceeded(CryptoTrackerError):
    """Raised when the crypto exchange API restricts access."""
    def __init__(self, retry_after: int) -> None:
        super().__init__(f"Cooldown active for {retry_after} seconds", retry_after)

class ConnectionTimeout(CryptoTrackerError):
    """Raised when the socket ghosting strikes."""
    def __init__(self, endpoint: str) -> None:
        super().__init__(f"Endpoint {endpoint} went dark", endpoint)

class ValidationError(CryptoTrackerError):
    """Raised when input data defies logic."""
    def __init__(self, field: str, reason: str) -> None:
        super().__init__(f"Invalid field {field}: {reason}", {"field": field, "reason": reason})

class DataInconsistency(CryptoTrackerError):
    """Raised when price feeds diverge wildly."""
    def __init__(self, exchange: str, delta: float) -> None:
        super().__init__(f"Price divergence at {exchange} of {delta}%", delta)