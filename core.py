import sys

def validate_crypto_input(data):
    required = {'symbol', 'price'}
    if not all(k in data for k in required):
        raise ValueError(f'missing keys: {required - data.keys()}')
    if not isinstance(data['price'], (int, float)) or data['price'] < 0:
        raise ValueError('price must be positive numeric')
    return True

def process_stream(data_stream):
    for entry in data_stream:
        try:
            if validate_crypto_input(entry):
                print(f'Processing {entry["symbol"]} at ${entry["price"]}')
        except (ValueError, TypeError) as e:
            print(f'Ignored malformed payload: {e}', file=sys.stderr)

if __name__ == '__main__':
    mock_data = [
        {'symbol': 'BTC', 'price': 65000},
        {'symbol': 'ETH', 'price': 'invalid'},
        {'symbol': 'SOL', 'price': 150},
        {'invalid': 'data'}
    ]
    process_stream(mock_data)