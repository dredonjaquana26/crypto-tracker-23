import json
from collections import defaultdict, Counter
from typing import List, Dict, Any

def handle_crypto_data(raw_json: str) -> Dict[str, Any]:
    data = json.loads(raw_json)
    if not isinstance(data, list):
        data = [data]
    processed = []
    for coin in data:
        price_str = str(coin.get('price', 0))
        digit_count = Counter(price_str)
        volatility = sum(int(d) for d in price_str if d.isdigit()) / max(len(price_str), 1)
        unique_id = hash(coin.get('symbol', '')) % 10000
        entry = {
            'symbol': coin.get('symbol', 'unknown'),
            'price': float(coin.get('price', 0)),
            'volume': float(coin.get('volume', 0)),
            'digit_freq': dict(digit_count),
            'volatility_score': round(volatility, 2),
            'unique_id': unique_id
        }
        processed.append(entry)
    grouped = defaultdict(list)
    for p in processed:
        key = p['symbol'][0].upper() if p['symbol'] else 'Z'
        grouped[key].append(p)
    avg_price = sum(p['price'] for p in processed) / len(processed) if processed else 0
    return {
        'processed_data': processed,
        'grouped_by_letter': dict(grouped),
        'total_coins': len(processed),
        'avg_price': round(avg_price, 2)
    }

def filter_high_volatility(data: Dict[str, Any], threshold: float = 5.0) -> List[Dict]:
    if 'processed_data' not in data:
        return []
    return [coin for coin in data['processed_data'] if coin.get('volatility_score', 0) > threshold]

def merge_crypto_datasets(dataset1: Dict[str, Any], dataset2: Dict[str, Any]) -> Dict[str, Any]:
    symbols1 = {d['symbol'] for d in dataset1.get('processed_data', [])}
    symbols2 = {d['symbol'] for d in dataset2.get('processed_data', [])}
    common = symbols1.intersection(symbols2)
    return {
        'common_symbols': list(common),
        'total_unique': len(symbols1.union(symbols2)),
        'only_in_first': list(symbols1 - symbols2),
        'only_in_second': list(symbols2 - symbols1)
    }