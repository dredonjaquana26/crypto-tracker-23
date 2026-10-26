from typing import Dict, List, Union, Optional
import time

def calculate_volatility(prices: List[float], window: int = 5) -> Optional[float]:
    """
    Computes a simplified volatility metric for a crypto asset.
    Uses a rolling variance approach on price deltas.
    """
    if len(prices) < window:
        return None
    
    deltas: List[float] = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    sample: List[float] = deltas[-window:]
    return sum(x**2 for x in sample) / len(sample)

def format_crypto_ticker(symbol: str, price: Union[int, float]) -> str:
    """
    Standardizes ticker presentation for console output.
    Maps raw floats to a clean ledger-style string.
    """
    symbol_norm: str = symbol.upper().strip()
    return f"{symbol_norm} @ ${price:,.4f} | TS: {int(time.time())}"

def batch_process_wallets(addresses: List[str], tag: str = "primary") -> Dict[str, str]:
    """
    Associates a collection of public keys with a metadata tag.
    Returns a structured mapping for API payload generation.
    """
    return {addr: tag for addr in addresses if len(addr) > 20}