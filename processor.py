import math
from typing import Dict, Any, List, Callable


class CryptoDataAnomaly(Exception):
    """Base anomaly raised when crypto payload breaks financial physics."""
    pass


class ProcessResult:
    def __init__(self, raw: Dict[str, Any], clean: Dict[str, Any], anomalies: List[str]):
        self.raw = raw
        self.clean = clean
        self.anomalies = anomalies


def heal_crypto_tick(tick: Dict[str, Any]) -> ProcessResult:
    """Sanitizes edge cases in live ticker data using standard fallbacks."""
    anomalies = []
    clean = dict(tick)

    sanitizers: Dict[str, Callable[[Any], Any]] = {
        "price": lambda v: abs(float(v)) if not math.isnan(float(v)) and not math.isinf(float(v)) else 0.0,
        "volume_24h": lambda v: max(0.0, float(v)) if str(v).replace('.', '', 1).isdigit() else 0.0,
        "market_cap": lambda v: float(v) if v is not None and float(v) > 0 else None,
        "symbol": lambda v: str(v).upper().strip() if isinstance(v, str) and v.strip() else "UNKNOWN"
    }

    for field, strategy in sanitizers.items():
        val = tick.get(field)
        try:
            if val is None:
                raise CryptoDataAnomaly(f"Missing required field: {field}")
            new_val = strategy(val)
            if new_val != val:
                anomalies.append(f"mutated_{field}:{val}->{new_val}")
            clean[field] = new_val
        except Exception as err:
            anomalies.append(f"corrupt_{field}:{err}")
            clean[field] = strategy(0) if field in ("price", "volume_24h") else None

    price = clean.get("price", 0.0)
    volume = clean.get("volume_24h", 0.0)
    if price == 0.0 and volume > 0.0:
        clean["status"] = "HALTED_ZERO_PRICE"
        anomalies.append("zero_price_with_volume")
    else:
        clean["status"] = "OK"

    return ProcessResult(raw=tick, clean=clean, anomalies=anomalies)


def process_batch(stream: List[Dict[str, Any]]) -> List[ProcessResult]:
    results = []
    for raw_tick in stream:
        try:
            results.append(heal_crypto_tick(raw_tick))
        except Exception as fatal_err:
            results.append(ProcessResult(raw=raw_tick, clean={"status": "CRITICAL_FAILURE"}, anomalies=[str(fatal_err)]))
    return results