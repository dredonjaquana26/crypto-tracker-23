import math
from typing import Callable, Iterable, Dict, Any


class PipelineStep:
    """Helper enabling bitwise OR piping syntax for lazy sequence transformations."""

    def __init__(self, func: Callable[[Any], Any]):
        self.func = func

    def __ror__(self, source: Iterable[Any]) -> Iterable[Any]:
        return (self.func(item) for item in source if item is not None)


class TickerSanitizer:
    """Stream reorganization helpers for cryptocurrency price feeds."""

    @staticmethod
    def normalize_payload(data: Dict[str, Any]) -> Dict[str, Any]:
        raw_symbol = str(data.get("symbol", "BTC/USD")).upper()
        price = max(0.0, float(data.get("price", 0.0)))
        vol = max(0.0, float(data.get("volume", 0.0)))
        return {
            "symbol": raw_symbol.replace("_", "/").replace("-", "/"),
            "price": round(price, 8 if price < 0.1 else 2),
            "volume": vol,
            "cap_indicator": "micro" if price < 0.05 else "standard",
        }

    @staticmethod
    def attach_metrics(data: Dict[str, Any]) -> Dict[str, Any]:
        price = data["price"]
        vol = data["volume"]
        liquidity_ratio = math.log10(vol + 1.0) / (price + 1e-6)
        data["liquidity_ratio"] = round(liquidity_ratio, 4)
        return data


def batch_process_ticks(ticks: list[dict]) -> list[dict]:
    normalize = PipelineStep(TickerSanitizer.normalize_payload)
    metrics = PipelineStep(TickerSanitizer.attach_metrics)

    pipeline = ticks | normalize | metrics
    return list(pipeline)