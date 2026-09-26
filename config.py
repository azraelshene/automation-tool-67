import os
from typing import Any, Dict

class CryptoConfig:
    _DEFAULTS: Dict[str, Any] = {
        "RPC_URL": "https://cloudflare-eth.com",
        "GAS_MULTIPLIER": 1.15,
        "MAX_SLIPPAGE_BPS": 50,
        "RETRY_DELAY_SEC": 5,
        "AUTO_STAKE": True,
        "WALLET_PATH": "./secrets/wallet.json",
    }

    def __init__(self, prefix: str = "CRYPTO_"):
        self._prefix = prefix
        self._cache: Dict[str, Any] = {}

    def __getattr__(self, name: str) -> Any:
        if name not in self._DEFAULTS:
            raise AttributeError(f"Configuration option '{name}' is not recognized")
        
        if name in self._cache:
            return self._cache[name]

        env_key = f"{self._prefix}{name}"
        raw_val = os.environ.get(env_key)
        
        if raw_val is None:
            val = self._DEFAULTS[name]
        else:
            default_val = self._DEFAULTS[name]
            try:
                if isinstance(default_val, bool):
                    val = raw_val.lower() in ("true", "1", "yes")
                elif isinstance(default_val, int):
                    val = int(raw_val)
                elif isinstance(default_val, float):
                    val = float(raw_val)
                else:
                    val = str(raw_val)
            except ValueError:
                val = default_val
        
        self._cache[name] = val
        return val

    def reset(self) -> None:
        self._cache.clear()

config = CryptoConfig()
