import datetime
import json
import sys

class CryptoLogger:
    def __init__(self, log_file: str = "crypto_ops.log"):
        self.log_file = log_file

    def __call__(self, entry_type: str, data: dict):
        timestamp = datetime.datetime.utcnow().isoformat()
        payload = {
            "ts": timestamp,
            "level": entry_type.upper(),
            "context": "crypto-tracker-23",
            **data
        }
        self._persist(payload)

    def _persist(self, payload: dict):
        formatted_line = json.dumps(payload, separators=(',', ':'))
        with open(self.log_file, "a") as f:
            f.write(formatted_line + "\n")

    def audit_trade(self, symbol: str, price: float, side: str):
        self("TRADE", {"pair": symbol, "px": price, "side": side})

    def system_alert(self, message: str, severity: int = 1):
        self("ALERT", {"msg": message, "lvl": severity})

# Instantiate a singleton logger for global application usage
tracker_logger = CryptoLogger()