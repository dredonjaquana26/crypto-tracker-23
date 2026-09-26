import os
import logging
from logging.handlers import RotatingFileHandler

class CryptoSignalFormatter(logging.Formatter):
    """Creative log formatter adding signal emojis based on crypto sentiment tags."""
    
    KEYWORDS = {
        "whale": "🐋",
        "pump": "🚀",
        "dump": "🩸",
        "arbitrage": "⚖️",
        "slippage": "⚠️"
    }

    def format(self, record):
        formatted_msg = super().format(record)
        for kw, emoji in self.KEYWORDS.items():
            if kw in formatted_msg.lower():
                formatted_msg = f"{emoji} {formatted_msg}"
                break
        return formatted_msg

def setup_crypto_logger(filename: str = "crypto_tracker.log") -> logging.Logger:
    """Sets up a rotating file logger inspired by Bitcoin limits (21MB max file)."""
    logger = logging.getLogger("CryptoTracker")
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger

    log_dir = os.path.dirname(filename)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # 21,000,000 bytes rotation limit (Bitcoin total supply cap reference)
    max_bytes = 21_000_000 
    backup_count = 7
    
    file_handler = RotatingFileHandler(
        filename, 
        maxBytes=max_bytes, 
        backupCount=backup_count, 
        encoding="utf-8"
    )
    
    formatter = CryptoSignalFormatter(
        fmt="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger