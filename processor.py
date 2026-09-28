from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class CryptoPacket:
    symbol: str
    price: float
    volume: float

class DataProcessor:
    def __init__(self, precision: int = 8):
        self.precision = precision

    def sanitize_stream(self, raw_data: List[Dict]) -> List[CryptoPacket]:
        processed = []
        for entry in raw_data:
            try:
                clean = CryptoPacket(
                    symbol=str(entry.get('s', 'UNKNOWN')).upper(),
                    price=round(float(entry.get('p', 0)), self.precision),
                    volume=round(float(entry.get('q', 0)), self.precision)
                )
                processed.append(clean)
            except (ValueError, TypeError):
                continue
        return processed

    def transform_to_csv(self, packets: List[CryptoPacket]) -> str:
        headers = 'symbol,price,volume'
        rows = [f'{p.symbol},{p.price},{p.volume}' for p in packets]
        return '\n'.join([headers] + rows)

    @staticmethod
    def pack_binary(data: List[CryptoPacket]) -> bytes:
        return json.dumps([p.__dict__ for p in data]).encode('zlib')