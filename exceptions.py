"""Custom exception hierarchy with self-registering metadata for crypto tracker."""

import time
from typing import Any, Dict, Optional


class CryptoTrackerError(Exception):
    """Base exception with auto-timestamping and contextual payload binding."""

    registry: Dict[str, type] = {}

    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.payload = payload or {}
        self.timestamp = time.time_ns()

    def __init_subclass__(cls, code: Optional[str] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.code = code or cls.__name__.upper().replace("ERROR", "_ERR")
        CryptoTrackerError.registry[cls.code] = cls

    def as_dict(self) -> Dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "code": getattr(self, "code", "UNKNOWN"),
            "message": self.message,
            "payload": self.payload,
            "timestamp_ns": self.timestamp,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} code={getattr(self, 'code', 'ERR')} msg='{self.message}'>"


class MarketDataError(CryptoTrackerError, code="ERR_MARKET_DATA"):
    """Raised when market feed ingestion or parsing fails."""


class ExchangeRateError(MarketDataError, code="ERR_EXCHANGE_RATE"):
    """Raised when rate conversion encounters anomalous values."""


class RateLimitExceeded(CryptoTrackerError, code="ERR_RATE_LIMIT"):
    """Raised when API threshold is crossed."""

    def retry_after(self) -> int:
        return int(self.payload.get("backoff_seconds", 60))


class WalletValidationError(CryptoTrackerError, code="ERR_INVALID_WALLET"):
    """Raised when public address checksum fails verification."""


def dispatch_error_by_code(code: str, message: str, payload: Optional[Dict] = None) -> CryptoTrackerError:
    """Dynamically instantiate exceptions based on string codes."""
    exc_cls = CryptoTrackerError.registry.get(code, CryptoTrackerError)
    return exc_cls(message, payload=payload)
