from datetime import datetime, timezone
from typing import Iterator, Dict, Any, Optional, NamedTuple
from decimal import Decimal, ROUND_HALF_UP


class CryptoTick(NamedTuple):
    symbol: str
    price: Decimal
    volume: Decimal
    timestamp: float


class DynamicTickPipeline:
    """Stream transformer for heterogeneous crypto ticker streams."""

    def __init__(self, precision: int = 8):
        self.precision = precision
        self._quantize_str = f"0.{'0' * (precision - 1)}1" if precision > 1 else "0.1"

    def __call__(self, feed: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        """Process stream of raw ticks into enriched crypto tick payloads."""
        for raw in feed:
            normalized = self._normalize_raw_dict(raw)
            if normalized:
                yield normalized

    def _normalize_raw_dict(self, raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        sym = raw.get("symbol") or raw.get("s") or raw.get("product_id")
        price_raw = raw.get("price") or raw.get("p") or raw.get("last")
        vol_raw = raw.get("volume") or raw.get("v") or raw.get("size") or "0"
        ts_raw = raw.get("timestamp") or raw.get("T") or raw.get("time")

        if not sym or price_raw is None:
            return None

        try:
            price = Decimal(str(price_raw)).quantize(
                Decimal(self._quantize_str), rounding=ROUND_HALF_UP
            )
            volume = Decimal(str(vol_raw)).quantize(
                Decimal(self._quantize_str), rounding=ROUND_HALF_UP
            )

            if isinstance(ts_raw, (int, float)):
                ts = float(ts_raw) if ts_raw < 1e11 else float(ts_raw) / 1000.0
            else:
                ts = datetime.now(timezone.utc).timestamp()

            tick = CryptoTick(
                symbol=str(sym).upper().replace("-", "").replace("_", ""),
                price=price,
                volume=volume,
                timestamp=ts,
            )

            return {
                "pair": tick.symbol,
                "metrics": {
                    "price": float(tick.price),
                    "volume": float(tick.volume),
                    "notional": float(tick.price * tick.volume),
                },
                "iso_time": datetime.fromtimestamp(tick.timestamp, tz=timezone.utc).isoformat(),
            }
        except (ValueError, TypeError, ArithmeticError):
            return None


def parse_crypto_stream(stream_data: list, precision: int = 4) -> list:
    """Utility function to transform raw exchange payloads into standard schema."""
    pipeline = DynamicTickPipeline(precision=precision)
    return list(pipeline(iter(stream_data)))
