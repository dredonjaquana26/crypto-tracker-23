import math
from decimal import Decimal, ROUND_HALF_UP
from typing import Union, Dict, List, Any


class CryptoFormatter:
    """Creative helper for formatting and converting crypto units fluently."""
    
    DECIMALS: Dict[str, int] = {
        "btc": 8,
        "eth": 18,
        "sats": 0,
        "gwei": 9,
        "usdt": 2
    }

    def __init__(self, raw_value: Union[int, float, str]):
        self._value = Decimal(str(raw_value))

    def to_units(self, unit: str) -> Decimal:
        """Convert raw base units to human-readable denomination."""
        decimals = self.DECIMALS.get(unit.lower(), 8)
        factor = Decimal(10) ** decimals
        target_precision = "1." + "0" * min(decimals, 8) if decimals > 0 else "1"
        return (self._value / factor).quantize(Decimal(target_precision), rounding=ROUND_HALF_UP)

    def format_currency(self, symbol: str = "$") -> str:
        """Format value as fiat currency with proper commas."""
        val = self._value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{symbol}{val:,.2f}"

    def __gt__(self, other: Any) -> bool:
        return self._value > Decimal(str(other))


def calculate_pnl(buy_price: float, current_price: float, quantity: float) -> Dict[str, float]:
    """Calculate profit/loss metrics with percentage and net return."""
    initial_cost = buy_price * quantity
    current_val = current_price * quantity
    net_pnl = current_val - initial_cost
    pct_change = ((current_price - buy_price) / buy_price * 100) if buy_price else 0.0
    return {
        "initial_cost": round(initial_cost, 4),
        "current_value": round(current_val, 4),
        "net_pnl": round(net_pnl, 4),
        "percentage": round(pct_change, 2)
    }


def chunk_symbols(symbols: List[str], chunk_size: int = 50) -> List[List[str]]:
    """Yield sliding batch chunks for API rate-limiting compliance."""
    return [symbols[i:i + chunk_size] for i in range(0, len(symbols), chunk_size)]
