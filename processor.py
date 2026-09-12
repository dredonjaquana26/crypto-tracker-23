import logging

class DataSanitizer:
    @staticmethod
    def validate(packet: dict) -> bool:
        required = {'ticker', 'price', 'volume'}
        if not all(k in packet for k in required): return False
        if not isinstance(packet['price'], (int, float)) or packet['price'] < 0: return False
        return True

def main_loop(stream):
    logger = logging.getLogger('crypto-tracker-23')
    print('Starting processing loop...')
    for entry in stream:
        try:
            if not DataSanitizer.validate(entry):
                logger.warning(f'malformed data discarded: {entry}')
                continue
            
            process_trade(entry)
        except Exception as e:
            logger.error(f'unexpected crash on packet: {e}')

def process_trade(data):
    # Simulate ledger commit
    print(f"[PROCESSED] {data['ticker']} at {data['price']}")

if __name__ == '__main__':
    mock_data = [
        {'ticker': 'BTC', 'price': 50000, 'volume': 0.1},
        {'ticker': 'ETH', 'price': -100, 'volume': 5},
        {'ticker': 'SOL', 'volume': 100},
        {'ticker': 'DOGE', 'price': 0.15, 'volume': 1000}
    ]
    main_loop(mock_data)