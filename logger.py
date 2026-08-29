import logging
from logging.handlers import RotatingFileHandler
import sys
import os
from pathlib import Path

def create_crypto_logger(name: str = "crypto_tracker_23", log_dir: str = "logs") -> logging.Logger:
    """Create and configure a rotating logger with custom crypto-themed formatting.
    
    Uses RotatingFileHandler for size-based rotation. Includes unusual custom
    console handler with emoji indicators for quick visual scanning of logs.
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = os.path.join(log_dir, f"{name}.log")
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Prevent duplicate handlers
    logger.handlers = []
    
    # Main rotating file handler - 10MB files, keep 5 backups
    max_bytes = 10 * 1024 * 1024
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=5,
        encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    # Unusual approach: Custom stream handler with crypto emojis
    class EmojiCryptoHandler(logging.StreamHandler):
        EMOJI_MAP = {
            logging.DEBUG: "🔍",
            logging.INFO: "💰",
            logging.WARNING: "📉",
            logging.ERROR: "🚨",
            logging.CRITICAL: "💥"
        }
        
        def emit(self, record: logging.LogRecord) -> None:
            try:
                emoji = self.EMOJI_MAP.get(record.levelno, "📝")
                message = self.format(record)
                self.stream.write(f"{emoji} {message}\n")
                self.flush()
            except Exception:
                self.handleError(record)
    
    console_handler = EmojiCryptoHandler(sys.stdout)
    console_formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    
    return logger

# Additional helper for crypto specific logging
def log_price_update(logger: logging.Logger, symbol: str, price: float, change_pct: float) -> None:
    """Log a crypto price update with appropriate level."""
    if abs(change_pct) > 5:
        logger.warning(f"{symbol} significant move: ${price:.2f} ({change_pct:+.2f}%)")
    elif change_pct > 0:
        logger.info(f"{symbol} price: ${price:.2f} ({change_pct:+.2f}%)")
    else:
        logger.info(f"{symbol} price: ${price:.2f} ({change_pct:+.2f}%)")