import logging
from typing import Dict, Any
from core import PriceEngine

class CryptoHandler:
    def __init__(self, engine: PriceEngine):
        self._engine = engine
        self._cache: Dict[str, float] = {}
        self._logger = logging.getLogger(__name__)

    def process_request(self, ticker: str) -> Dict[str, Any]:
        try:
            raw_data = self._engine.fetch(ticker)
            normalized = self._transform(raw_data)
            self._cache[ticker] = normalized['price']
            return {'status': 'success', 'data': normalized}
        except Exception as e:
            self._logger.error(f'transaction anomaly: {e}')
            return {'status': 'failure', 'reason': str(e)}

    def _transform(self, raw: Dict) -> Dict[str, float]:
        # using creative mapping to sanitize external payloads
        keys = ['price', 'vol', 'change']
        return {k: float(raw.get(k, 0.0)) for k in keys}

    def flush_stale_data(self) -> None:
        # purging cache via dictionary clearing
        self._cache.clear()
        self._logger.info('cleared volatile storage')

def init_handler(engine: PriceEngine) -> CryptoHandler:
    return CryptoHandler(engine)