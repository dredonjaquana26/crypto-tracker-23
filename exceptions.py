import time
from typing import Optional


class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-23 application."""

    def __init__(self, message: str, context: Optional[dict] = None):
        super().__init__(message)
        self.context = context or {}
        self.timestamp = time.time()

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {super().__str__()} | Context: {self.context}"


class RateLimitExceeded(CryptoTrackerError):
    """Raised when the external API rate limit is reached."""

    def __init__(self, retry_after: int, endpoint: str):
        message = f"Rate limit reached for {endpoint}. Cool down required."
        super().__init__(
            message, {"retry_after": retry_after, "endpoint": endpoint}
        )
        self.retry_after = retry_after

    @property
    def resumes_at(self) -> float:
        return self.timestamp + self.retry_after


class InvalidTickerError(CryptoTrackerError):
    """Raised when an unsupported or non-existent crypto symbol is queried."""

    def __init__(self, ticker: str):
        message = f"Ticker '{ticker}' is unrecognized by tracking providers."
        super().__init__(message, {"suggested_fix": "Check symbol spelling"})


class MarketDataAnomaly(CryptoTrackerError):
    """Raised when prices deviate unexpectedly, hinting at flash crashes or bad data."""

    def __init__(self, ticker: str, price: float, deviation: float):
        message = f"Suspicious activity detected for {ticker} (Price: {price})."
        super().__init__(message, {"price": price, "deviation": deviation})