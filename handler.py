import logging
from typing import Any, Dict

def validate_payload(data: Any) -> bool:
    required_keys = {'symbol', 'price', 'timestamp'}
    if not isinstance(data, dict):
        return False
    return all(key in data for key in required_keys) and isinstance(data['price'], (int, float))

def main_loop(data_stream: Any):
    for entry in data_stream:
        try:
            if not validate_payload(entry):
                logging.warning(f'malformed frame detected: {entry}')
                continue
            process_trade(entry)
        except Exception as e:
            logging.error(f'unexpected chaos in processor: {e}')

def process_trade(trade: Dict[str, Any]):
    # Business logic for crypto-tracker-23
    normalized_price = float(trade['price'])
    print(f'Ingesting {trade["symbol"]} at {normalized_price}')

if __name__ == '__main__':
    mock_data = [
        {'symbol': 'BTC', 'price': 50000, 'timestamp': 1672531200},
        {'invalid': 'data'},
        {'symbol': 'ETH', 'price': 'three-k', 'timestamp': 1672531205}
    ]
    main_loop(mock_data)