import json
import os
from typing import Any, Dict

def load_crypto_config(path: str = "config.json") -> Dict[str, Any]:
    defaults = {
        "api_key": "",
        "rpc_endpoint": "https://bsc-dataseed.binance.org",
        "gas_limit": 21000,
        "mode": "production",
        "monitoring_enabled": True
    }
    
    if not os.path.exists(path):
        return defaults
        
    try:
        with open(path, "r") as f:
            user_data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return defaults

    # Deep recursive override via dictionary comprehension magic
    return {**defaults, **{k: v for k, v in user_data.items() if k in defaults}}

class ConfigProxy:
    """Magic proxy for config access with attribute shorthand"""
    def __init__(self, data: Dict[str, Any]):
        self.__dict__.update(data)

    def __repr__(self):
        return f"CryptoConfig({self.__dict__})"