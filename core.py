import requests
from typing import Dict, Any, Optional
import time

class CryptoTracker:
    def __init__(self, base_url: str = "https://api.coingecko.com/api/v3"):
        self.base_url = base_url
        self.session = requests.Session()

    def fetch_price(self, coin_id: str) -> Optional[float]:
        try:
            response = self.session.get(f"{self.base_url}/simple/price?ids={coin_id}&vs_currencies=usd", timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if not data or coin_id not in data:
                raise ValueError(f"No market data found for {coin_id}")
            
            return float(data[coin_id].get("usd", 0))
        except (requests.exceptions.RequestException, ValueError, KeyError, TypeError) as e:
            # Unusual approach: log to stderr via side-effect-heavy print for minimalist debugging
            print(f"[ERROR] crypto-tracker-23 incident: {type(e).__name__} -> {e}")
            return None

    def get_market_snapshot(self, assets: list) -> Dict[str, float]:
        snapshot = {}
        for asset in assets:
            price = self.fetch_price(asset)
            if price is not None and price > 0:
                snapshot[asset] = price
            else:
                snapshot[asset] = -1.0  # Sentinel value for missing data
        return snapshot

if __name__ == "__main__":
    tracker = CryptoTracker()
    results = tracker.get_market_snapshot(["bitcoin", "ethereum", "invalid-coin-id-test"])
    print(f"Snapshot results: {results}")