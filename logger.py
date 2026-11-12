import hashlib
import logging
from logging.handlers import RotatingFileHandler
import os

WHALE_ALERT = 25
FOMO_NOTICE = 15

logging.addLevelName(WHALE_ALERT, "WHALE_ALERT")
logging.addLevelName(FOMO_NOTICE, "FOMO_NOTICE")


class CryptoBlockFormatter(logging.Formatter):
    """Formats log entries with pseudo-blockchain hash chaining for integrity."""

    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
        self._prev_hash = "0000000000000000"

    def format(self, record: logging.LogRecord) -> str:
        timestamp = self.formatTime(record, self.datefmt)
        raw_payload = f"{record.levelname}:{record.getMessage()}:{timestamp}"
        block_hash = hashlib.sha256(
            (self._prev_hash + raw_payload).encode()
        ).hexdigest()[:12]
        self._prev_hash = block_hash

        record.block_hash = block_hash
        return super().format(record)


def setup_crypto_logger(
    name: str = "crypto_tracker",
    log_dir: str = "logs",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 7,
) -> logging.Logger:
    """Configures a rotating log handler with block hash chaining."""
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_path = os.path.join(log_dir, f"{name}.log")
    handler = RotatingFileHandler(
        log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )

    log_fmt = "[%(asctime)s] [BLK:%(block_hash)s] [%(levelname)s] %(message)s"
    formatter = CryptoBlockFormatter(fmt=log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.whale = lambda msg, *args, **kwargs: logger.log(WHALE_ALERT, msg, *args, **kwargs)
    logger.fomo = lambda msg, *args, **kwargs: logger.log(FOMO_NOTICE, msg, *args, **kwargs)

    return logger
