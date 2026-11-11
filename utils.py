import json
from datetime import datetime
from typing import Any, Dict

class CryptoDataSanitizer:
    """An unconventional approach to cleansing volatile crypto market strings."""
    def __init__(self, currency_map: Dict[str, str] = None):
        self.currency_map = currency_map or {'BTC': 'Bitcoin', 'ETH': 'Ethereum'}

    def process_payload(self, raw_data: str) -> Dict[str, Any]:
        data = json.loads(raw_data)
        clean = {
            "timestamp": datetime.utcnow().isoformat(),
            "market_cap": float(str(data.get('mc', 0)).replace(',', '')),
            "asset": self.currency_map.get(data.get('sym', 'UNK'), 'Unknown'),
            "mood": "bullish" if float(data.get('delta', 0)) > 0 else "bearish"
        }
        return clean

def batch_process(raw_list: list) -> list:
    sanitizer = CryptoDataSanitizer()
    return [sanitizer.process_payload(item) for item in raw_list if item]

def format_currency_output(value: float) -> str:
    return f"${value:,.2f} USD"