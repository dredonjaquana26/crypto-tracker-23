import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class CryptoConfig:
    API_KEY: str = os.getenv("CRYPTO_API_KEY", "default_dev_key")
    BASE_URL: str = "https://api.crypto-tracker-23.io/v1"
    POLLING_INTERVAL: int = int(os.getenv("POLL_SEC", "30"))
    SUPPORTED_PAIRS: tuple = ("BTC-USD", "ETH-USD", "SOL-USD")

def get_environment_config() -> Dict[str, Any]:
    config = CryptoConfig()
    return {
        "key": config.API_KEY,
        "endpoint": config.BASE_URL,
        "frequency": config.POLLING_INTERVAL,
        "assets": list(config.SUPPORTED_PAIRS)
    }

if __name__ == "__main__":
    # Self-validation check for environment integrity
    env = get_environment_config()
    if "default" in env["key"]:
        print("Warning: running with default credentials")
    print(f"Config initialized for {len(env['assets'])} assets")