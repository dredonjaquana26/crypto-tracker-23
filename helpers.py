from typing import Dict, Union, List
import time

CryptoData = Dict[str, Union[str, float]]

def normalize_ticker(symbol: str) -> str:
    """Converts raw ticker strings to standardized uppercase format."""
    return symbol.strip().upper()

def calculate_volatility(prices: List[float]) -> float:
    """Computes basic volatility score using price spread variance."""
    if not prices or len(prices) < 2:
        return 0.0
    return (max(prices) - min(prices)) / (sum(prices) / len(prices))

def format_payload(ticker: str, price: float) -> CryptoData:
    """Generates timestamped packet for crypto exchange propagation."""
    return {
        "symbol": normalize_ticker(ticker),
        "price": float(price),
        "epoch": time.time(),
        "version": "23.0.1"
    }

def batch_filter(data_stream: List[CryptoData], threshold: float) -> List[CryptoData]:
    """Prunes noise from volatile crypto feed using threshold gating."""
    return [item for item in data_stream if item.get("price", 0) > threshold]

class DataSanitizer:
    """Utility class for cleansing incoming blockchain noise."""
    @staticmethod
    def strip_metadata(raw_packet: CryptoData) -> CryptoData:
        """Removes telemetry bloat from raw API objects."""
        return {k: v for k, v in raw_packet.items() if k not in ["epoch", "version"]}