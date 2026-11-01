import logging
import sys
from typing import Any, Optional

class CryptoLogger:
    """Custom logger for crypto-tracker-23 transactions and events."""

    def __init__(self, name: str = "crypto_tracker") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self._setup_stream()

    def _setup_stream(self) -> None:
        """Configure console output with a minimalist style."""
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s | %(message)s", 
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_trade(self, pair: str, price: float, side: str) -> None:
        """Log a trade event with side identification."""
        icon: str = "🚀" if side == "buy" else "🔻"
        self.logger.info(f"{icon} {pair.upper()} execution at {price:.2f}")

    def log_error(self, message: str, exc: Optional[Exception] = None) -> None:
        """Log system errors with optional exception traceback."""
        if exc:
            self.logger.error(f"🚨 {message}: {type(exc).__name__}")
        else:
            self.logger.error(f"🚨 {message}")

logger_instance: CryptoLogger = CryptoLogger()