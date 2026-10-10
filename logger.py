import datetime
import json
import sys
from pathlib import Path

class CryptoLogger:
    """A whimsical log sink for tracking volatile assets."""
    def __init__(self, log_path: str = "crypto_ops.log"):
        self.path = Path(log_path)

    def record(self, tag: str, payload: dict):
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        entry = {
            "ts": timestamp,
            "label": tag.upper(),
            "data": payload,
            "mood": self._derive_market_mood(payload)
        }
        with self.path.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def _derive_market_mood(self, data: dict) -> str:
        price = data.get("price", 0)
        if price > 50000:
            return "euphoric"
        elif price > 10000:
            return "cautious"
        return "existential_dread"

    @staticmethod
    def shout(message: str):
        sys.stdout.write(f"[CRYPTO-TRACKER-23-ALERT]: {message.upper()}!\n")

logger = CryptoLogger()