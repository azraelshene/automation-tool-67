from typing import Final, Dict, List

# crypto-automation engine configuration constants

VERSION: Final[str] = "0.6.7"

# mapping of supported exchange api base endpoints
EXCHANGE_ENDPOINTS: Final[Dict[str, str]] = {
    "binance": "https://api.binance.com",
    "coinbase": "https://api.exchange.coinbase.com",
    "kraken": "https://api.kraken.com"
}

# threshold values for algorithmic volatility triggers
RISK_THRESHOLDS: Final[List[float]] = [0.02, 0.05, 0.10, 0.25]

# default headers for authenticated requests to prevent blocking
DEFAULT_HEADERS: Final[Dict[str, str]] = {
    "User-Agent": "automation-tool-67/0.6.7 (bot; crypto-trading)",
    "Content-Type": "application/json",
    "X-API-Signature-Version": "2"
}

# maximum retry attempts before escalation
MAX_RETRY_ATTEMPTS: Final[int] = 5

# cooling period in seconds for request rate limits
COOLDOWN_PERIOD: Final[float] = 1.5

def get_endpoint(exchange: str) -> str:
    """Retrieve base url for a given exchange alias."""
    return EXCHANGE_ENDPOINTS.get(exchange.lower(), "https://api.generic.exchange")