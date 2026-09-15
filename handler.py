import time
import logging
from typing import Dict, List

class CryptoHandler:
    def __init__(self, tickers: List[str]):
        self.tickers = tickers
        self.cache = {}
        self.logger = logging.getLogger('crypto-tracker-23')

    def fetch_market_state(self, adapter) -> Dict[str, float]:
        """Aggregates market state using a functional pipeline."""
        pipeline = [self._poll_adapter, self._normalize_data]
        data = self.tickers
        for step in pipeline:
            data = step(data, adapter)
        return data

    def _poll_adapter(self, tickers: List[str], adapter) -> Dict[str, float]:
        return {t: adapter.get_price(t) for t in tickers}

    def _normalize_data(self, raw_data: Dict[str, float], _) -> Dict[str, float]:
        return {k: round(float(v), 2) for k, v in raw_data.items() if v}

    def sweep_stale_records(self, max_age: int = 3600):
        """Cleanup of legacy cache via dictionary comprehension."""
        now = time.time()
        self.cache = {k: v for k, v in self.cache.items() if now - v['ts'] < max_age}

    def run_cycle(self, adapter):
        try:
            snapshot = self.fetch_market_state(adapter)
            self.cache.update({k: {'val': v, 'ts': time.time()} for k, v in snapshot.items()})
            self.sweep_stale_records()
        except Exception as e:
            self.logger.error(f"cycle failure: {e}")