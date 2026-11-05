import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, filepath: str = 'config.json'):
        self.filepath = filepath
        self.defaults = {
            'api_base': 'https://api.exchange.com',
            'refresh_interval': 60,
            'symbols': ['BTC', 'ETH']
        }

    def load(self) -> Dict[str, Any]:
        config = self.defaults.copy()
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    user_data = json.load(f)
                    config.update({k: v for k, v in user_data.items() if k in self.defaults})
            except (json.JSONDecodeError, IOError):
                pass
        return config

    def __getitem__(self, key: str) -> Any:
        return self.load().get(key)

config = ConfigLoader()