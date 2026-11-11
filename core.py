import sys

def validate_payload(data):
    if not isinstance(data, dict) or 'symbol' not in data:
        raise ValueError("Malformed crypto payload")
    if not data['symbol'].isalnum() or len(data['symbol']) > 5:
        raise ValueError("Invalid ticker format")
    return True

def run_processor(stream):
    print("Starting crypto-tracker-23 engine...")
    for entry in stream:
        try:
            if validate_payload(entry):
                price = entry.get('price', 0)
                if price < 0:
                    raise ValueError("Negative pricing anomaly")
                process_trade(entry)
        except (ValueError, TypeError) as e:
            print(f"Sanitization failure: {e}")
            continue

def process_trade(data):
    # Simulate atomic ledger write
    print(f"Ledger update: {data['symbol']} @ {data['price']}")

if __name__ == '__main__':
    mock_stream = [
        {'symbol': 'BTC', 'price': 50000},
        {'symbol': 'INVALID_TOKEN_NAME', 'price': 10},
        {'symbol': 'ETH', 'price': -5},
        {'symbol': 'SOL', 'price': 100}
    ]
    run_processor(mock_stream)