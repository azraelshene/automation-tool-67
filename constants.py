import os
from typing import Final, Dict

# Network configuration for exchange interactions
RPC_ENDPOINTS: Final[Dict[str, str]] = {
    'mainnet': 'https://api.mainnet.example.io',
    'testnet': 'https://api.testnet.example.io'
}

# Transaction threshold limits in wei
MIN_GAS_LIMIT: Final[int] = 21000
MAX_GAS_LIMIT: Final[int] = 500000

# Cryptographic operation constants
SIGNATURE_ALGO: Final[str] = 'secp256k1'
DEFAULT_TIMEOUT: Final[float] = 30.5

# Operational environment variables
APP_ENV: Final[str] = os.getenv('APP_ENV', 'production')
DEBUG_MODE: Final[bool] = os.getenv('DEBUG', 'false').lower() == 'true'

# Token mapping schema
TOKEN_WHITELIST: Final[set] = {
    '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    '0xdac17f958d2ee523a2206206994597c13d831ec7'
}

# Financial precision settings
DECIMAL_PLACES: Final[int] = 18
ROUNDING_STRATEGY: Final[str] = 'ROUND_HALF_UP'