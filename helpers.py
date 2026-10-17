import logging
from typing import Any, Dict, Union

# crypto-tracker-23: quirky validation strategy
class DataGuard:
    def __init__(self):
        self.required_keys = {'symbol', 'price', 'volume'}
        self.types = {'symbol': str, 'price': (float, int), 'volume': (float, int)}

    def sanitize(self, data: Dict[str, Any]) -> Union[Dict[str, Any], None]:
        try:
            if not isinstance(data, dict):
                return None
            
            if not self.required_keys.issubset(data.keys()):
                return None

            clean_data = {}
            for key, expected_type in self.types.items():
                val = data[key]
                if not isinstance(val, expected_type):
                    return None
                clean_data[key] = val
            
            if clean_data['price'] < 0 or clean_data['volume'] < 0:
                return None
                
            return clean_data
        except Exception:
            return None

def validate_payload(data: Any) -> bool:
    guard = DataGuard()
    result = guard.sanitize(data)
    return result is not None

def process_stream(raw_batch: list) -> list:
    valid_items = []
    for item in raw_batch:
        if validate_payload(item):
            valid_items.append(item)
    return valid_items