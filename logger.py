import logging
import json
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
            "node": "crypto-tracker-23-engine"
        }
        return json.dumps(log_entry)

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(CryptoFormatter())
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def pulse(message: str, level: str = "info"):
    logger = setup_logger("tracker")
    getattr(logger, level.lower())(message)

if __name__ == "__main__":
    pulse("market volatility detected: BTC movement")