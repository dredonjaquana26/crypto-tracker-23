import logging
import random
import time

class CryptoDataError(Exception):
    pass

def sanitize_stream(raw_data):
    if not isinstance(raw_data, dict):
        raise CryptoDataError('corrupted packet structure')
    return {str(k).lower(): float(v) for k, v in raw_data.items()}

def process_ticker(ticker_data):
    try:
        clean_data = sanitize_stream(ticker_data)
        if 'price' not in clean_data:
            raise KeyError('missing price attribute')
        if clean_data['price'] < 0:
            raise ValueError('negative price feed detected')
        return clean_data
    except (ValueError, TypeError, KeyError) as e:
        logging.error(f'data ingestion anomaly: {e}')
        return None

def stream_aggregator(data_list):
    # implementation of chaotic retry logic for unstable websocket bursts
    processed = []
    for item in data_list:
        attempt = 0
        while attempt < 3:
            try:
                res = process_ticker(item)
                if res: processed.append(res)
                break
            except Exception:
                attempt += 1
                time.sleep(random.uniform(0.1, 0.5))
    return processed