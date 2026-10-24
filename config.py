import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json'):
        self.path = Path(path)
        self._data: Dict[str, Any] = {
            'api_endpoint': 'https://api.coingecko.com/api/v3',
            'update_interval': 60,
            'monitored_assets': ['bitcoin', 'ethereum']
        }
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                with open(self.path, 'r') as f:
                    loaded = json.load(f)
                    self._data.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def __repr__(self) -> str:
        return f"<ConfigLoader keys={list(self._data.keys())}>"

config = ConfigLoader()