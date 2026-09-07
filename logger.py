import logging
from logging.handlers import RotatingFileHandler

class CryptoFormatter(logging.Formatter):
    LEVEL_EMOJIS = {
        logging.DEBUG: "🔍",
        logging.INFO: "🚀",
        logging.WARNING: "⚠️",
        logging.ERROR: "🚨",
        logging.CRITICAL: "💥"
    }

    def format(self, record):
        emoji = self.LEVEL_EMOJIS.get(record.levelno, "📝")
        record.msg = f"{emoji} {record.msg}"
        return super().format(record)

def setup_logger(name="crypto_tracker", log_file="tracker.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=1024*1024, backupCount=3, encoding="utf-8"
        )
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_formatter = CryptoFormatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger

if __name__ == "__main__":
    log = setup_logger()
    log.debug("Scanning market pairs...")
    log.info("Bitcoin surged past resistance!")
    log.warning("High volatility detected on ETH/USDT")
    log.error("Failed to fetch order book from API")