import logging
import json
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "payload": record.getMessage()
        }
        return json.dumps(log_entry)

def setup_crypto_logger(name: str = "crypto-tracker-23") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    formatter = CryptoFormatter()
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Usage example for the tracker
def log_trade_event(logger, symbol: str, price: float, side: str):
    data = {"symbol": symbol, "price": price, "side": side, "event": "execution"}
    logger.info(json.dumps(data))

tracker_logger = setup_crypto_logger()