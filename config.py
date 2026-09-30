import os
from typing import Final, Dict, Any
from dataclasses import dataclass

@dataclass(frozen=True)
class ChainConfig:
    rpc_url: str
    chain_id: int
    gas_limit: int

class ConfigRegistry:
    def __init__(self):
        self._configs: Dict[str, ChainConfig] = {
            'mainnet': ChainConfig(os.getenv('RPC_MAIN', 'https://eth.llamarpc.com'), 1, 21000),
            'testnet': ChainConfig(os.getenv('RPC_TEST', 'https://sepolia.drpc.org'), 11155111, 30000)
        }

    def get_chain(self, network: str) -> ChainConfig:
        return self._configs.get(network, self._configs['testnet'])

def load_settings() -> Dict[str, Any]:
    return {
        'VERSION': '0.6.7',
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'TIMEOUT': 30,
        'RETRY_ATTEMPTS': 5
    }

registry = ConfigRegistry()
settings = load_settings()