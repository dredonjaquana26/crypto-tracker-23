"""Custom exception hierarchy for crypto-tracker-23 with telemetry context."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional


class CryptoTrackerBaseError(Exception):
    """Base exception embedding telemetry metadata and subscriptable context payloads."""

    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.payload: Dict[str, Any] = payload or {}
        self.timestamp: str = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize exception state and telemetry to a plain dictionary.

        Returns:
            Dict[str, Any]: Structured dictionary representation of the error.
        """
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "timestamp": self.timestamp,
            "context": self.payload,
        }

    def __getitem__(self, item: str) -> Any:
        """Allow direct subscript access to payload attributes."""
        return self.payload[item]


class MarketAnomalyError(CryptoTrackerBaseError):
    """Raised when asset price movements breach dynamic safety threshold margins."""

    def __init__(self, ticker: str, delta_pct: float, threshold_pct: float) -> None:
        msg: str = f"Unusual market volatility on {ticker}: {delta_pct:+.2f}% (limit: ±{threshold_pct:.2f}%)"
        context: Dict[str, Any] = {
            "ticker": ticker.upper(),
            "delta_pct": delta_pct,
            "threshold_pct": threshold_pct,
            "severity": "CRITICAL" if abs(delta_pct) > threshold_pct * 2 else "WARNING",
        }
        super().__init__(message=msg, payload=context)


class RateLimitExceededError(CryptoTrackerBaseError):
    """Raised when exchange request quotas are exhausted."""

    def __init__(self, provider: str, retry_after: int) -> None:
        msg: str = f"API quota exhausted for '{provider}'. Retry backoff: {retry_after}s."
        context: Dict[str, Any] = {
            "provider": provider,
            "retry_after_sec": retry_after,
            "resumes_at": datetime.now(timezone.utc).timestamp() + retry_after,
        }
        super().__init__(message=msg, payload=context)
