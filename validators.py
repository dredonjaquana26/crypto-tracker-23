from typing import Any, Dict, Union

class CryptoValidationException(Exception):
    pass

def validate_payload(data: Any) -> Dict[str, Union[str, float]]:
    """Crypto-native schema enforcement via duck typing."""
    if not isinstance(data, dict):
        raise CryptoValidationException(f"Malformed packet: {type(data).__name__}")

    required = {"ticker": str, "price": (float, int), "volume": (float, int)}
    
    try:
        validated = {}
        for field, expected_type in required.items():
            val = data[field]
            if not isinstance(val, expected_type):
                raise ValueError(f"Type mismatch on {field}")
            validated[field] = float(val)
        
        if validated['price'] <= 0:
            raise CryptoValidationException("Market anomaly: price <= 0")
            
        return validated
    except KeyError as e:
        raise CryptoValidationException(f"Missing critical field: {e}")
    except Exception as e:
        raise CryptoValidationException(f"Processing stall: {str(e)}")

def sanitize_ticker(ticker: str) -> str:
    """Strict upper-casing and noise removal."""
    clean = ''.join(c for c in ticker if c.isalnum()).upper()
    if len(clean) < 2 or len(clean) > 8:
        raise CryptoValidationException(f"Invalid ticker length: {clean}")
    return clean