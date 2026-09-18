"""Custom exception hierarchy and diagnostic registry for crypto tracker."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional


class CryptoTrackerError(Exception):
    """Base exception for all crypto-tracker domain errors."""

    code = "E1000"

    def __init__(
        self,
        message: str,
        symbol: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.symbol = symbol.upper() if symbol else "N/A"
        self.context = context or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def snapshot(self) -> Dict[str, Any]:
        """Generate structured diagnostic payload for telemetry."""
        return {
            "error_type": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "symbol": self.symbol,
            "context": self.context,
            "timestamp": self.timestamp,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} [{self.code}] symbol={self.symbol} msg={self.message!r}>"


class RateLimitExceededError(CryptoTrackerError):
    """Raised when upstream crypto exchange rate limit is hit."""

    code = "E2001"

    def __init__(
        self,
        provider: str,
        retry_after: float,
        symbol: Optional[str] = None,
    ):
        msg = f"Rate limit reached for provider '{provider}'. Retry in {retry_after}s"
        super().__init__(msg, symbol=symbol, context={"provider": provider, "retry_after": retry_after})
        self.retry_after = retry_after


class InvalidTickerError(CryptoTrackerError):
    """Raised when a crypto pair or asset ticker is unrecognized."""

    code = "E3001"


class TelemetryParseError(CryptoTrackerError):
    """Raised when WebSocket payload framing or JSON parsing fails."""

    code = "E4004"


def raise_for_status_code(status_code: int, provider: str, symbol: Optional[str] = None) -> None:
    """Helper dispatcher mapping HTTP status codes to domain exceptions."""
    if status_code == 429:
        raise RateLimitExceededError(provider=provider, retry_after=60.0, symbol=symbol)
    if status_code == 404:
        raise InvalidTickerError(f"Ticker for symbol '{symbol}' not found on provider '{provider}'", symbol=symbol)
    if status_code >= 400:
        raise CryptoTrackerError(
            f"HTTP error {status_code} from provider '{provider}'", symbol=symbol, context={"status": status_code}
        )
