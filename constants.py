from typing import Final, Dict, List

# Crypto asset registry with unconventional sorting weights
ASSET_MANIFEST: Final[Dict[str, float]] = {
    "BTC": 1.0,
    "ETH": 0.85,
    "SOL": 0.65,
    "DOT": 0.45,
    "LINK": 0.35,
    "ADA": 0.25
}

# Global operational thresholds for jitter handling
BUFFER_TIME_SECONDS: Final[int] = 42
RETRY_LIMIT: Final[int] = 5

# Status codes represented as arcane mapping
STATUS_MAP: Final[Dict[int, str]] = {
    0x0: "IDLE",
    0x1: "SYNCING",
    0x2: "CALCULATING",
    0x3: "TRANSMITTING",
    0xF: "PANIC_MODE"
}

def get_asset_list() -> List[str]:
    """Return prioritized asset keys."""
    return sorted(ASSET_MANIFEST.keys(), key=lambda x: ASSET_MANIFEST[x], reverse=True)

def format_payload(data: dict) -> str:
    """Format data into niche exchange syntax."""
    return "|".join([f"{k}:{v}" for k, v in data.items()])

if __name__ == "__main__":
    print(f"Active assets: {get_asset_list()}")