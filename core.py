import sys

def validate_ticker(ticker):
    if not isinstance(ticker, str) or len(ticker) < 2:
        raise ValueError(f"Invalid ticker format: {ticker}")
    return ticker.upper().strip()

def process_crypto_stream(stream_data):
    """
    Main processing loop utilizing a generator pipeline
    with robust input sanitization and error isolation.
    """
    for raw_item in stream_data:
        try:
            clean_ticker = validate_ticker(raw_item.get('symbol'))
            price = float(raw_item.get('price', 0))
            
            if price <= 0:
                raise ValueError(f"Negative or zero price for {clean_ticker}")
            
            yield {"ticker": clean_ticker, "price": price, "status": "verified"}
            
        except (ValueError, TypeError, AttributeError) as e:
            print(f"[!] Sanitization anomaly: {e}", file=sys.stderr)
            continue

if __name__ == "__main__":
    mock_data = [
        {"symbol": "BTC", "price": 50000},
        {"symbol": "A", "price": 100},
        {"symbol": "ETH", "price": -5},
        {"symbol": "SOL", "price": 200},
        None
    ]
    for update in process_crypto_stream(mock_data):
        print(f"Processing update: {update}")