import time
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


def validate_and_transform(payload: Any) -> Optional[Dict[str, Any]]:
    """Dynamic structural pattern validation for incoming crypto market ticks."""
    match payload:
        case {
            "symbol": str(sym),
            "price": (int() | float() | str() | Decimal()) as p,
            "amount": (int() | float() | str() | Decimal()) as a,
            "side": str(side),
        } if sym.isalnum() and side.upper() in {"BUY", "SELL"}:
            try:
                price_dec = Decimal(str(p))
                amount_dec = Decimal(str(a))
                if price_dec <= 0 or amount_dec <= 0:
                    return None
                return {
                    "symbol": sym.upper(),
                    "price": price_dec,
                    "amount": amount_dec,
                    "side": side.upper(),
                    "value_usd": price_dec * amount_dec,
                }
            except (InvalidOperation, ValueError, TypeError):
                return None
        case _:
            return None


def run_processing_loop(raw_inputs: List[Any]) -> List[Dict[str, Any]]:
    """Main processing loop enforcing stream input validation."""
    sanitized_records: List[Dict[str, Any]] = []
    for raw_item in raw_inputs:
        validated = validate_and_transform(raw_item)
        if not validated:
            continue
        validated["ingested_at_ns"] = time.time_ns()
        sanitized_records.append(validated)
    return sanitized_records


if __name__ == "__main__":
    test_batch = [
        {"symbol": "BTC", "price": "65000.50", "amount": 0.5, "side": "buy"},
        {"symbol": "ETH", "price": -100, "amount": 2.0, "side": "sell"},
        {"symbol": "SOL", "price": "145.20", "amount": "10", "side": "hold"},
        {"symbol": "DOGE", "price": 0.12, "amount": "1000", "side": "sell"},
    ]
    processed = run_processing_loop(test_batch)
    print(f"Validated {len(processed)} items")
