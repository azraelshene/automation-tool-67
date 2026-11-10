import os
import json
from pathlib import Path
from collections import ChainMap
from typing import Any, Dict

CRYPTO_DEFAULTS = {
    "network": "ethereum",
    "chain_id": 1,
    "rpc_url": "https://eth.llamarpc.com",
    "gas_limit_multiplier": 1.15,
    "max_fee_per_gas_gwei": 50.0,
    "slippage_tolerance": 0.005,
    "auto_approve": False,
    "min_liquidity_usd": 10000.0,
}

class CryptoConfig:
    """Dynamic configuration loader merging env vars, file overrides, and crypto defaults."""
    def __init__(self, config_path: str | None = None):
        file_cfg = {}
        target_path = Path(config_path or "config.json")
        if target_path.exists():
            with open(target_path, "r", encoding="utf-8") as f:
                file_cfg = json.load(f)
        
        env_cfg = {}
        for k, v in os.environ.items():
            if k.startswith("CRYPTO_"):
                key_name = k.replace("CRYPTO_", "").lower()
                env_cfg[key_name] = v
        
        self._store = ChainMap(env_cfg, file_cfg, CRYPTO_DEFAULTS)

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            val = self._store[name]
            default_val = CRYPTO_DEFAULTS.get(name)
            if default_val is not None and not isinstance(val, type(default_val)):
                try:
                    if isinstance(default_val, bool):
                        return str(val).lower() in ("true", "1", "yes")
                    return type(default_val)(val)
                except (ValueError, TypeError):
                    return default_val
            return val
        raise AttributeError(f"Configuration parameter '{name}' is undefined")

    def snapshot(self) -> Dict[str, Any]:
        return {key: getattr(self, key) for key in self._store.keys()}
