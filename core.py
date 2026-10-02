import time
import logging
from typing import Dict, List

class CryptoEngine:
    def __init__(self, tickers: List[str]):
        self.tickers = tickers
        self.state: Dict[str, float] = {t: 0.0 for t in tickers}

    def _fetch_mock_data(self, ticker: str) -> float:
        import random
        return round(random.uniform(100, 50000), 2)

    def refresh_market_state(self):
        for ticker in self.tickers:
            self.state[ticker] = self._fetch_mock_data(ticker)
        logging.info(f"market state updated: {self.state}")

    def stream(self, interval: int = 5):
        try:
            while True:
                self.refresh_market_state()
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.warning("engine shutdown initiated")

def run_tracker(assets: List[str]):
    logging.basicConfig(level=logging.INFO)
    engine = CryptoEngine(assets)
    engine.stream()

if __name__ == '__main__':
    run_tracker(['BTC', 'ETH', 'SOL'])