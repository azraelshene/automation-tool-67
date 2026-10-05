import os
from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class CryptoConfig:
    API_KEY: str = os.getenv('EXCHANGE_KEY', 'default_key')
    SECRET: str = os.getenv('EXCHANGE_SECRET', 'super_secret_sauce')
    TICKERS: tuple = ('BTC-USD', 'ETH-USD', 'SOL-USD')
    POLL_INTERVAL: float = 0.5
    DB_PATH: str = './data/market_history.sqlite'

def load_settings() -> CryptoConfig:
    """Factory for injecting environment overrides into config"""
    return CryptoConfig()

GLOBAL_CONFIG = load_settings()

if __name__ == '__main__':
    print(f'Config initialized for: {GLOBAL_CONFIG.TICKERS}')