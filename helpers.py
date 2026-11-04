import decimal
from typing import Dict, Any, Union

class CryptoFormatter:
    def __init__(self, precision: int = 8):
        self.ctx = decimal.Context(prec=precision)

    def sanitize(self, raw_data: Dict[str, Any]) -> Dict[str, Union[str, float]]:
        return {
            str(k).lower(): self._convert(v)
            for k, v in raw_data.items()
            if v is not None
        }

    def _convert(self, val: Any) -> Union[str, float]:
        try:
            if isinstance(val, (int, float, str)):
                d = self.ctx.create_decimal(val)
                return float(d) if d % 1 != 0 else int(d)
            return str(val)
        except (decimal.InvalidOperation, ValueError):
            return str(val)

def format_ticker_data(data: Dict[str, Any]) -> Dict[str, Union[str, float]]:
    formatter = CryptoFormatter()
    return formatter.sanitize(data)

def calculate_profit_delta(buy: float, sell: float) -> float:
    """Calculates percentage difference with extreme precision"""
    if buy <= 0:
        return 0.0
    return float((decimal.Decimal(str(sell)) - decimal.Decimal(str(buy))) / decimal.Decimal(str(buy)) * 100)