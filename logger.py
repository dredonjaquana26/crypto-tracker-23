import logging
from typing import Any, Optional

class CryptoLogger:
    """Custom logger for crypto-tracker-23 with dramatic flair."""
    def __init__(self, name: str = "crypto_node") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler: logging.StreamHandler = logging.StreamHandler()
        fmt: logging.Formatter = logging.Formatter(
            "[%(asctime)s] ₿ %(levelname)s: %(message)s", 
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(fmt)
        self.logger.addHandler(handler)

    def alert(self, msg: str, data: Optional[Any] = None) -> None:
        """Log critical market fluctuations with style."""
        payload: str = f" {data}" if data else ""
        self.logger.warning(f"MARKET_SHOCK: {msg}{payload}")

    def track(self, event: str) -> None:
        """Track blockchain sync events silently."""
        self.logger.info(f"SYNC_EVENT: {event}")

def get_logger(name: str = "crypto_tracker") -> CryptoLogger:
    """Factory for standardized logger instances."""
    return CryptoLogger(name)