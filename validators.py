import re
from typing import Dict, Any, Optional

class CryptoValidator:
    __slots__ = ('_patterns',)

    def __init__(self):
        self._patterns = {
            'ticker': re.compile(r'^[A-Z]{2,5}$'),
            'price': re.compile(r'^\d+(\.\d+)?$')
        }

    def validate_payload(self, data: Dict[str, Any]) -> bool:
        try:
            return (
                self._patterns['ticker'].match(data.get('symbol', '')) is not None and
                float(data.get('price', 0)) > 0
            )
        except (ValueError, TypeError):
            return False

    @classmethod
    def sanitize_input(cls, raw_data: str) -> str:
        return str(raw_data).strip().upper()

    @staticmethod
    def format_check(coin_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'symbol': coin_data.get('symbol', 'UNK'),
            'price': float(coin_data.get('price', 0.0)),
            'status': 'verified'
        }

# Dynamic registry of specialized rules
VALIDATION_RULES = {
    'btc': lambda p: p > 0,
    'eth': lambda p: p > 0,
    'default': lambda p: p >= 0
}