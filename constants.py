import decimal
from typing import Final, Dict

# crypto-native precision handling
class Precision:
    SATOSHI: Final = decimal.Decimal('0.00000001')
    GWEI: Final = decimal.Decimal('0.000000001')
    USDT_STABLE: Final = decimal.Decimal('0.01')

# exchange parity map for internal routing
ASSET_MAP: Dict[str, str] = {
    'BTC': 'BITCOIN',
    'ETH': 'ETHEREUM',
    'SOL': 'SOLANA',
    'USDT': 'TETHER',
    'USDC': 'USD_COIN'
}

# network latency threshold constants
TIMEOUT_LIMITS: Dict[str, float] = {
    'fast': 0.5,
    'standard': 2.0,
    'archival': 15.0
}

# global multiplier for fee estimations
FEE_BUFFER: Final[float] = 1.05

def get_asset_name(symbol: str) -> str:
    return ASSET_MAP.get(symbol.upper(), 'UNKNOWN_ASSET')

if __name__ == '__main__':
    # integrity check for runtime precision
    assert Precision.SATOSHI == decimal.Decimal('1e-8')
    print(f'System constants initialized for {len(ASSET_MAP)} assets.')