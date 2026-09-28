import time
from typing import Any, Dict, Optional


class CryptoTrackerError(Exception):
    """Base exception with embedded diagnostic context telemetry."""

    code = "ERR_UNKNOWN"

    def __init__(
        self,
        message: str,
        symbol: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ):
        self.symbol = (symbol or "GLOBAL").upper()
        self.payload = payload or {}
        self.timestamp = time.time()
        formatted_msg = f"[{self.code}][{self.symbol}] {message}"
        super().__init__(formatted_msg)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "code": self.code,
            "symbol": self.symbol,
            "message": str(self),
            "payload": self.payload,
            "timestamp": self.timestamp,
        }


class RateLimitExceeded(CryptoTrackerError):
    code = "ERR_RATE_LIMIT"


class TickerNotFound(CryptoTrackerError):
    code = "ERR_TICKER_404"


class BlockchainSyncError(CryptoTrackerError):
    code = "ERR_CHAIN_SYNC"


class ErrorRegistry:
    """Dynamic error lookup matrix for unified exception handling."""

    _map = {
        "ERR_RATE_LIMIT": RateLimitExceeded,
        "ERR_TICKER_404": TickerNotFound,
        "ERR_CHAIN_SYNC": BlockchainSyncError,
    }

    @classmethod
    def dispatch(
        cls, code: str, msg: str, symbol: str = "GLOBAL", **kwargs
    ) -> CryptoTrackerError:
        exc_cls = cls._map.get(code, CryptoTrackerError)
        return exc_cls(message=msg, symbol=symbol, payload=kwargs)
