import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, filepath: str = 'settings.json'):
        self.filepath = filepath
        self.defaults = {
            'rpc_node': 'https://bsc-dataseed.binance.org/',
            'gas_limit': 200000,
            'retry_attempts': 3,
            'debug_mode': False
        }

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.filepath):
            return self.defaults
        
        with open(self.filepath, 'r') as f:
            try:
                user_data = json.load(f)
            except json.JSONDecodeError:
                return self.defaults

        return {**self.defaults, **{k: v for k, v in user_data.items() if k in self.defaults}}

    def __getattr__(self, name: str) -> Any:
        config = self.load()
        if name in config:
            return config[name]
        raise AttributeError(f'No configuration key: {name}')

settings = ConfigLoader()