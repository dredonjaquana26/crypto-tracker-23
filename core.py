import sys

def validate_payload(data):
    required = {'symbol': str, 'price': (int, float)}
    if not isinstance(data, dict) or not all(k in data for k in required):
        return False
    return all(isinstance(data[k], v) for k, v in required.items())

def main_loop(stream):
    for event in stream:
        try:
            if not validate_payload(event):
                raise ValueError(f"malformed crypto event: {event}")
            
            process_tick(event)
        except (ValueError, TypeError) as e:
            print(f"skip tainted data: {e}", file=sys.stderr)

def process_tick(data):
    # Core business logic for crypto-tracker-23
    print(f"processing {data['symbol']} @ {data['price']}")

if __name__ == "__main__":
    # Simulate ingestion stream
    mock_stream = [
        {'symbol': 'BTC', 'price': 60000},
        {'symbol': 'ETH', 'price': 'invalid'},
        {'symbol': 'SOL', 'price': 150}
    ]
    main_loop(mock_stream)