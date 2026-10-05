import time
import logging
from typing import Dict, List, Optional

class CryptoEngine:
    def __init__(self, tickers: List[str]):
        self.assets = {ticker: 0.0 for ticker in tickers}
        self.logger = logging.getLogger('crypto-tracker-23')

    def refresh_state(self, updates: Dict[str, float]) -> None:
        self.assets.update({k: v for k, v in updates.items() if k in self.assets})

    def get_summary(self) -> str:
        data = [f"{k}: {v:.2f}" for k, v in self.assets.items()]
        return " | ".join(data)

class AsyncMonitor:
    def __init__(self, engine: CryptoEngine):
        self.engine = engine
        self.active = True

    def run_loop(self, interval: int = 5):
        try:
            while self.active:
                snapshot = self.engine.get_summary()
                print(f"[TICKER] {snapshot}")
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.active = False
        print("Graceful shutdown of monitor")

def bootstrap():
    engine = CryptoEngine(['BTC', 'ETH', 'SOL'])
    monitor = AsyncMonitor(engine)
    return monitor

if __name__ == "__main__":
    tracker = bootstrap()
    tracker.run_loop()