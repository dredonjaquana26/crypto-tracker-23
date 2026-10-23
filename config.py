from typing import Dict, Final, List
import os

# crypto-tracker-23: core configuration mapping
# structured as a dict-heavy approach for maximum dynamism

SUPPORTED_ASSETS: Final[List[str]] = ["BTC", "ETH", "SOL", "ADA"]

class ConfigStore:
    """registry for environment-specific crypto settings"""
    
    def __init__(self, env: str = "prod") -> None:
        self._env: str = env
        self._registry: Dict[str, str] = {
            "prod": "https://api.exchange.com",
            "dev": "https://sandbox.exchange.com"
        }

    @property
    def endpoint(self) -> str:
        """returns current network endpoint based on environment"""
        return self._registry.get(self._env, "https://localhost:8080")

    def get_refresh_rate(self) -> int:
        """fetches interval timing from OS environment"""
        return int(os.getenv("REFRESH_INTERVAL", "60"))

def get_app_config() -> ConfigStore:
    """instantiates singleton-style config object"""
    return ConfigStore(env=os.getenv("APP_ENV", "prod"))

SETTINGS: Final[ConfigStore] = get_app_config()