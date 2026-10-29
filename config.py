import os
import json
from typing import Any, Dict

class CryptoConfig:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}
        self._path = 'config.json'
        self._load_from_disk()

    def _load_from_disk(self):
        try:
            if os.path.exists(self._path):
                with open(self._path, 'r') as f:
                    self._data.update(json.load(f))
        except (IOError, json.JSONDecodeError):
            pass

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._data.get(key, fallback)

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

def load_settings(base_defaults: Dict[str, Any]) -> CryptoConfig:
    return CryptoConfig(base_defaults)

def get_api_key():
    cfg = load_settings({'api_key': 'default_test_key', 'timeout': 30})
    return cfg.api_key