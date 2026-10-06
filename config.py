import os
import json
from typing import Any, Dict

class ConfigLoader:
    _DEFAULTS = {
        "api_key": "anonymous",
        "strategy": "scalping",
        "threshold": 0.05,
        "rpc_url": "https://mainnet.infura.io/v3/"
    }

    def __init__(self, path: str = "config.json"):
        self.path = path
        self.settings = self._load_and_merge()

    def _load_and_merge(self) -> Dict[str, Any]:
        data = self._DEFAULTS.copy()
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    file_data = json.load(f)
                    data.update({k: v for k, v in file_data.items() if k in self._DEFAULTS})
            except (json.JSONDecodeError, IOError):
                pass
        return data

    def __getitem__(self, key: str) -> Any:
        return self.settings.get(key)

    def __getattr__(self, name: str) -> Any:
        return self.settings.get(name)

    def reload(self):
        self.settings = self._load_and_merge()

config = ConfigLoader()