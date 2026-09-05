import logging
import json
from datetime import datetime

class CryptoLogger:
    def __init__(self, name: str = "crypto-tracker-23"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_trade(self, pair: str, price: float, side: str):
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "trade_execution",
            "details": {
                "pair": pair.upper(),
                "price": price,
                "side": side.lower()
            }
        }
        self.logger.info(json.dumps(payload))

    def alert(self, message: str, level: str = "critical"):
        prefix = "!!! ALERT !!!"
        output = f"{prefix} [{level.upper()}] -> {message}"
        self.logger.warning(output)

# Instantiate singleton for global usage
tracker_logger = CryptoLogger()