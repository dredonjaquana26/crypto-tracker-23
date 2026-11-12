import logging
import sys
from typing import Any, Dict

class CryptoLogger:
    """Custom logger for crypto-tracker-23 transactions."""

    def __init__(self, name: str = "crypto_tracker") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            "[%(asctime)s] | %(levelname)s | %(message)s", datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_trade(self, symbol: str, price: float, side: str) -> None:
        """Log execution of market orders with flair."""
        self.logger.info(f"Trade executed: {side.upper()} {symbol} at ${price:,.2f}")

    def alert_volatility(self, data: Dict[str, Any]) -> None:
        """Panic-mode logger for high volatility events."""
        if data.get("change", 0) > 0.05:
            self.logger.warning(f"High volatility detected on {data.get('symbol')}: {data.get('change'):.2%}")

    def debug_payload(self, packet: Any) -> None:
        """Raw dump for cryptic API responses."""
        self.logger.debug(f"Trace payload: {repr(packet)}")

# Global instance for project-wide use
tracker_log: CryptoLogger = CryptoLogger()