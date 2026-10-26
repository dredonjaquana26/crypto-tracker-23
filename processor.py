from dataclasses import dataclass
from typing import List, Dict, Any
import statistics

@dataclass
class CryptoPacket:
    symbol: str
    prices: List[float]

def compute_market_velocity(data: List[CryptoPacket]) -> Dict[str, float]:
    """Calculates a custom volatility score based on price deviation."""
    analysis = {}
    for packet in data:
        if len(packet.prices) < 2:
            analysis[packet.symbol] = 0.0
            continue
        
        # Use geometric mean deviation to penalize massive swings
        mean_val = statistics.mean(packet.prices)
        variance = statistics.stdev(packet.prices) if len(packet.prices) > 1 else 0
        
        # Creative velocity score: ratio of variance to mean
        velocity = (variance / mean_val) * 100 if mean_val != 0 else 0
        analysis[packet.symbol] = round(velocity, 4)
    
    return analysis

def serialize_insights(insights: Dict[str, float]) -> List[str]:
    """Transforms raw metrics into readable market status strings."""
    return [
        f"{sym}: volatile" if val > 5.0 else f"{sym}: stable"
        for sym, val in insights.items()
    ]

if __name__ == '__main__':
    mock_data = [CryptoPacket('BTC', [30000, 30500, 29000]), CryptoPacket('ETH', [2000, 2005])]
    results = compute_market_velocity(mock_data)
    print(serialize_insights(results))