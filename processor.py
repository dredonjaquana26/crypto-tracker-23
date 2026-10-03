import time
from typing import Dict, Any, Generator, Tuple

def validate_ticker(data: Dict[str, Any]) -> Tuple[bool, str]:
    # Lambda validation rules for crypto telemetry payloads
    rules = {
        "symbol": lambda v: isinstance(v, str) and v.isalnum() and 3 <= len(v) <= 8,
        "price": lambda v: isinstance(v, (int, float)) and v > 0,
        "volume": lambda v: isinstance(v, (int, float)) and v >= 0,
        "timestamp": lambda v: isinstance(v, (int, float)) and v <= time.time()
    }
    
    if not isinstance(data, dict):
        return False, "payload must be a dictionary"
        
    for key, validator in rules.items():
        if key not in data:
            return False, f"missing required field: {key}"
        if not validator(data[key]):
            return False, f"invalid value for field: {key} ({data[key]})"
            
    return True, "valid"

def transaction_processor() -> Generator[Dict[str, Any], Dict[str, Any], None]:
    """
    Main processing loop driven by coroutines to validate incoming stream payloads.
    """
    processed_count = 0
    anomaly_log = []
    
    while True:
        payload = yield {"status": "ready", "processed": processed_count, "anomalies": len(anomaly_log)}
        if payload is None:
            continue
            
        is_valid, reason = validate_ticker(payload)
        if is_valid:
            payload["symbol"] = payload["symbol"].upper()
            payload["processed_at"] = time.time()
            processed_count += 1
            yield {"status": "success", "data": payload}
        else:
            anomaly_log.append((payload, reason))
            yield {"status": "rejected", "reason": reason}