from typing import Dict, List, Optional, Union
import time

class CryptoHandler:
    def __init__(self, wallet_address: str, chain: str = "ethereum") -> None:
        """Initialize the handler with address and chain context."""
        self.wallet_address: str = wallet_address
        self.chain: str = chain
        self.cache: Dict[str, Union[float, int]] = {}

    def fetch_balance(self, asset: str) -> float:
        """Retrieve current asset balance via mocked rpc simulation."""
        # Simulate latency of an RPC call
        time.sleep(0.01)
        mock_data: Dict[str, float] = {"BTC": 0.45, "ETH": 12.3, "SOL": 150.0}
        balance: float = mock_data.get(asset.upper(), 0.0)
        self.cache[asset] = balance
        return balance

    def calculate_total_value(self, assets: List[str], prices: Dict[str, float]) -> float:
        """Compute portfolio valuation with current market prices."""
        total: float = 0.0
        for asset in assets:
            balance = self.fetch_balance(asset)
            total += balance * prices.get(asset.upper(), 0.0)
        return total

    def get_summary(self) -> Dict[str, Optional[Union[str, float]]]:
        """Generate snapshot of current handler state."""
        return {
            "address": self.wallet_address,
            "network": self.chain,
            "last_update": time.time(),
            "cached_assets": list(self.cache.keys())
        }