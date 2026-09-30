import decimal
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class CryptoMath:
    SATOSHI: Final = decimal.Decimal('0.00000001')
    GWEI: Final = decimal.Decimal('0.000000001')
    PRECISION_LIMIT: Final = 18

class ChainConstants:
    RPC_TIMEOUT: Final[int] = 30
    MAX_RETRIES: Final[int] = 3
    DEFAULT_PRECISION: Final[int] = 8

    @classmethod
    def get_context(cls):
        return decimal.Context(
            prec=cls.MAX_RETRIES * 10,
            rounding=decimal.ROUND_HALF_UP
        )

EXCHANGES = {
    'BINANCE': {'fee': '0.001', 'ws': 'wss://stream.binance.com:9443/ws'},
    'COINBASE': {'fee': '0.005', 'ws': 'wss://ws-feed.exchange.coinbase.com'}
}

def normalize_amount(amount: str | float) -> decimal.Decimal:
    ctx = ChainConstants.get_context()
    val = decimal.Decimal(str(amount))
    return val.quantize(ChainConstants.SATOSHI, context=ctx)

CRYPTO_MAP = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'SOL': 'Solana'
}