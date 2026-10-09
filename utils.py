from typing import Dict, List, Union, Optional
import hashlib

CryptoData = Dict[str, Union[str, float]]

def generate_asset_hash(asset: CryptoData) -> str:
    """Generates a deterministic unique hash for a crypto asset entry."""
    raw_string: str = f"{asset.get('symbol')}:{asset.get('price')}".lower()
    return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

def normalize_portfolio(assets: List[CryptoData]) -> Dict[str, float]:
    """Aggregates asset values by symbol into a compact mapping."""
    summary: Dict[str, float] = {}
    for entry in assets:
        symbol: str = str(entry.get('symbol', 'UNKNOWN'))
        value: float = float(entry.get('price', 0.0))
        summary[symbol] = summary.get(symbol, 0.0) + value
    return summary

def format_currency(amount: float, symbol: str = 'USD') -> str:
    """Constructs a display-ready string for financial data."""
    return f"{symbol} {amount:,.2f}"

def filter_high_value(assets: List[CryptoData], threshold: float) -> List[CryptoData]:
    """Extraction of assets exceeding a specific value threshold."""
    return [a for a in assets if float(a.get('price', 0.0)) > threshold]