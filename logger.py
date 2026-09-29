import os
import sys
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from datetime import datetime, timezone

class CryptoLogFormatter(logging.Formatter):
    """Custom log formatter injecting crypto-themed indicators and UTC timestamps."""
    
    INDICATORS = {
        logging.DEBUG: "🔍 [TICK]",
        logging.INFO: "📈 [MARKET]",
        logging.WARNING: "⚠️ [VOLATILE]",
        logging.ERROR: "💥 [LIQUIDATION]",
        logging.CRITICAL: "🚨 [SYSTEM_HALT]"
    }

    def format(self, record: logging.LogRecord) -> str:
        indicator = self.INDICATORS.get(record.levelno, "📝 [LOG]")
        utc_time = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        formatted_msg = f"{utc_time} UTC | {indicator} [{record.name}] {record.getMessage()}"
        if record.exc_info:
            formatted_msg += f"\n{self.formatException(record.exc_info)}"
        return formatted_msg


def setup_crypto_logger(
    name: str = "tracker",
    log_dir: str = "logs",
    max_bytes: int = 2 * 1024 * 1024,
    backup_count: int = 5
) -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        return logger

    formatter = CryptoLogFormatter()

    # Size-based rotation for high-frequency ticker feeds
    stream_file = os.path.join(log_dir, f"{name}_stream.log")
    size_handler = RotatingFileHandler(stream_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    size_handler.setLevel(logging.DEBUG)
    size_handler.setFormatter(formatter)

    # Midnight time-based rotation for audit trails
    audit_file = os.path.join(log_dir, f"{name}_audit.log")
    time_handler = TimedRotatingFileHandler(audit_file, when="MIDNIGHT", interval=1, backupCount=14, encoding="utf-8")
    time_handler.setLevel(logging.INFO)
    time_handler.setFormatter(formatter)

    # Console streaming for live stdout debugging
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(size_handler)
    logger.addHandler(time_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_crypto_logger()
