import time
from typing import Any, Callable, Generator, Dict


class StreamValidationError(ValueError):
    """Raised when incoming crypto stream record fails validation checks."""
    pass


def _check_symbol(payload: Dict[str, Any]) -> Dict[str, Any]:
    sym = str(payload.get("symbol", "")).upper().strip()
    if not sym or not sym.isalnum() or len(sym) > 12:
        raise StreamValidationError(f"invalid market ticker symbol: '{sym}'")
    payload["symbol"] = sym
    return payload


def _check_price(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        price = float(payload["price"])
        if price <= 0:
            raise StreamValidationError(f"non-positive price value: {price}")
        payload["price"] = round(price, 8)
        return payload
    except (KeyError, TypeError, ValueError) as err:
        raise StreamValidationError(f"malformed price field: {err}") from err


def _check_volume(payload: Dict[str, Any]) -> Dict[str, Any]:
    vol = payload.get("volume", 0.0)
    try:
        vol_float = float(vol)
        if vol_float < 0:
            raise StreamValidationError(f"negative volume detected: {vol_float}")
        payload["volume"] = vol_float
        return payload
    except (TypeError, ValueError) as err:
        raise StreamValidationError(f"invalid volume payload: {err}") from err


VALIDATION_PIPELINE: tuple[Callable[[Dict[str, Any]], Dict[str, Any]], ...] = (
    _check_symbol,
    _check_price,
    _check_volume,
)


def process_feed_stream(raw_batch: list[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    """Main loop executing dynamic functional validation pipe on stream payloads."""
    for item in raw_batch:
        if not isinstance(item, dict):
            continue

        record = item.copy()
        is_valid = True

        for stage in VALIDATION_PIPELINE:
            try:
                record = stage(record)
            except StreamValidationError as err:
                record["_valid"] = False
                record["_error"] = str(err)
                is_valid = False
                yield record
                break

        if is_valid:
            record["_valid"] = True
            record["ingested_at"] = time.time()
            yield record
