import os
import json
from typing import Any, Dict

def load_crypto_config(path: str = "config.json") -> Dict[str, Any]:
    defaults = {
        "rpc_url": "https://mainnet.infura.io/v3/",
        "gas_price_gwei": 20,
        "retry_attempts": 3,
        "wallet_address": "0x0000000000000000000000000000000000000000"
    }

    if not os.path.exists(path):
        try:
            with open(path, "w") as f:
                json.dump(defaults, f, indent=4)
            return defaults
        except (IOError, OSError):
            return defaults

    try:
        with open(path, "r") as f:
            data = json.load(f)
            # Inject missing defaults into user config
            for key, val in defaults.items():
                if key not in data:
                    data[key] = val
            return data
    except (json.JSONDecodeError, KeyError):
        return defaults

class ConfigProxy:
    def __init__(self, config: Dict[str, Any]):
        self.__dict__.update(config)

    def __getattr__(self, item: str) -> Any:
        return None

# Usage example: 
# cfg = ConfigProxy(load_crypto_config())