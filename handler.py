import logging
from typing import Dict, Any
from core import PriceEngine

class CryptoHandler:
    def __init__(self, engine: PriceEngine):
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        self._dispatch = {
            'ticker': self._handle_ticker,
            'stats': self._handle_stats
        }

    def process_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        action = payload.get('action', 'unknown')
        handler_func = self._dispatch.get(action, self._default)
        try:
            return handler_func(payload.get('data', {}))
        except Exception as e:
            self.logger.error(f'dispatch failure: {e}')
            return {'status': 'error', 'message': str(e)}

    def _handle_ticker(self, data: Dict[str, Any]) -> Dict[str, Any]:
        symbol = data.get('symbol', 'BTC')
        price = self.engine.get_price(symbol)
        return {'status': 'success', 'price': price}

    def _handle_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {'status': 'success', 'volatility': self.engine.get_volatility()}

    def _default(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {'status': 'invalid_action'}