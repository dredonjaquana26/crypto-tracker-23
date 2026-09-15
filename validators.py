import re

class CryptoValidationException(Exception):
    """Custom exception for crypto ticker anomalies."""
    pass

def validate_ticker(ticker: str) -> str:
    """
    Sanitizes and validates crypto tickers using a regex pattern.
    Rejects anything that isn't a 2-10 character alphanumeric string.
    """
    pattern = re.compile(r'^[A-Z0-9]{2,10}$')
    clean_ticker = str(ticker).strip().upper()

    if not pattern.match(clean_ticker):
        raise CryptoValidationException(f"Ticker '{clean_ticker}' failed sanity check")
    
    return clean_ticker

def validate_amount(amount: float) -> float:
    """
    Ensures the trade volume is non-negative and finite.
    """
    try:
        val = float(amount)
        if val < 0:
            raise ValueError("Negative amount")
    except (ValueError, TypeError):
        raise CryptoValidationException(f"Invalid numerical input: {amount}")
        
    return val

def process_payload(data: dict) -> dict:
    """
    Unconventional data gatekeeper for incoming crypto stream.
    """
    return {
        "symbol": validate_ticker(data.get("s", "")), 
        "quantity": validate_amount(data.get("q", 0)),
        "timestamp": data.get("t", "unknown")
    }