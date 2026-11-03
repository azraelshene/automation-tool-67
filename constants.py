import os
from typing import Final

# Network Endpoints
RPC_NODE: Final[str] = os.getenv('RPC_ENDPOINT', 'https://api.mainnet-beta.solana.com')
WS_ENDPOINT: Final[str] = os.getenv('WS_ENDPOINT', 'wss://api.mainnet-beta.solana.com')

# Crypto Constants
DECIMALS: Final[int] = 9
LAMPORT_MULTIPLIER: Final[int] = 10**DECIMALS

# Bot Behavioral Parameters
RETRY_ATTEMPTS: Final[int] = 3
TIMEOUT_SECONDS: Final[float] = 15.5
POLLING_INTERVAL: Final[float] = 0.5

# Transaction Metadata
PRIORITY_FEE_MICROLAMPORTS: Final[int] = 100_000
COMMITMENT_LEVEL: Final[str] = 'confirmed'

# Asset Identifiers (Mapped for internal lookup)
TOKEN_MAP: Final[dict[str, str]] = {
    'SOL': 'So11111111111111111111111111111111111111112',
    'USDC': 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
}

# Error/Status Codes
STATUS_SUCCESS: Final[str] = 'TX_CONFIRMED'
STATUS_FAILED: Final[str] = 'TX_REVERTED'
STATUS_PENDING: Final[str] = 'TX_MEMPOOL'