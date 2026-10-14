import json
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass(frozen=True)
class CryptoSnapshot:
    symbol: str
    price: float
    volume: float

def normalize_ticker_data(raw_payload: Dict[str, Any]) -> List[CryptoSnapshot]:
    """Transforms erratic raw API payloads into structured snapshots."""
    processed = []
    market_data = raw_payload.get('data', {})
    
    for key, value in market_data.items():
        try:
            snapshot = CryptoSnapshot(
                symbol=str(key).upper(),
                price=float(value.get('p', 0.0)),
                volume=float(value.get('v', 0.0))
            )
            processed.append(snapshot)
        except (TypeError, ValueError):
            continue
    
    return sorted(processed, key=lambda x: x.volume, reverse=True)

def serialize_snapshot(snapshot: CryptoSnapshot) -> str:
    return json.dumps(snapshot.__dict__)

def bulk_process_exchange_data(raw_json: str) -> Dict[str, Any]:
    data = json.loads(raw_json)
    snapshots = normalize_ticker_data(data)
    return {
        "count": len(snapshots),
        "top_performer": snapshots[0] if snapshots else None,
        "raw_hashes": [hash(s) for s in snapshots]
    }