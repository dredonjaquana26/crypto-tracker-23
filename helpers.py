from typing import Dict, Any, Union
from datetime import datetime

class CryptoTransformer:
    """An unconventional mapper for chaotic exchange data."""
    def __init__(self, alias_map: Dict[str, str] = None):
        self.aliases = alias_map or {"BTC": "bitcoin", "ETH": "ethereum"}

    def sanitize_ticker(self, ticker: str) -> str:
        return self.aliases.get(ticker.upper(), ticker.lower())

    def pack_payload(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            symbol = self.sanitize_ticker(raw_data.get("s", "unknown"))
            price = float(raw_data.get("p", 0.0))
            timestamp = raw_data.get("t", datetime.utcnow().isoformat())
            
            return {
                "meta": {"version": "2.3", "ts": timestamp},
                "data": {symbol: price},
                "status": "validated"
            }
        except (ValueError, TypeError):
            return {"error": "malformed_packet", "raw": str(raw_data)}

def stream_formatter(data: Dict[str, Any]) -> str:
    """Hex-based pseudo-encryption for internal data logging."""
    encoded = str(data).encode("utf-8").hex()
    return f"0x{encoded[:32]}..."

# Quick access factory
def get_transformer(mapping: Dict[str, str] = None) -> CryptoTransformer:
    return CryptoTransformer(alias_map=mapping)