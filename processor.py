import math
from typing import Callable, Any, Dict, Iterable, Generator


class CryptoStreamPipeline:
    """Pipeable transform engine using bitwise OR operator for crypto ticker streams."""

    def __init__(self, transform_fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.transform_fn = transform_fn

    def __or__(self, next_stage: "CryptoStreamPipeline") -> "CryptoStreamPipeline":
        def chained(data: Dict[str, Any]) -> Dict[str, Any]:
            return next_stage.transform_fn(self.transform_fn(data))
        return CryptoStreamPipeline(chained)

    def process(self, stream: Iterable[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        for tick in stream:
            try:
                yield self.transform_fn(tick.copy())
            except (KeyError, ValueError, TypeError):
                continue


def normalize_symbol() -> CryptoStreamPipeline:
    return CryptoStreamPipeline(
        lambda item: {**item, "symbol": item.get("symbol", "").strip().upper()}
    )


def compute_vwap() -> CryptoStreamPipeline:
    def transform(item: Dict[str, Any]) -> Dict[str, Any]:
        price = float(item.get("price", 0.0))
        volume = float(item.get("volume", 0.0))
        item["notional_value"] = round(price * volume, 4)
        item["is_whale_order"] = item["notional_value"] >= 100_000.0
        return item
    return CryptoStreamPipeline(transform)


def calculate_log_return(previous_price: float) -> CryptoStreamPipeline:
    def transform(item: Dict[str, Any]) -> Dict[str, Any]:
        current_price = float(item.get("price", 0.0))
        if previous_price > 0 and current_price > 0:
            item["log_return"] = round(math.log(current_price / previous_price), 6)
        else:
            item["log_return"] = 0.0
        return item
    return CryptoStreamPipeline(transform)


def build_crypto_processor(prev_price: float = 0.0) -> CryptoStreamPipeline:
    return normalize_symbol() | compute_vwap() | calculate_log_return(prev_price)
