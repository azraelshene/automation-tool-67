import hashlib
import hmac
import time
from typing import Dict, Any

class CryptoDataSanitizer:
    def __init__(self, secret: str):
        self._secret = secret.encode('utf-8')

    def sign_payload(self, data: Dict[str, Any]) -> str:
        """Generates a hmac signature for API payloads."""
        message = '&'.join([f'{k}={v}' for k, v in sorted(data.items())])
        return hmac.new(self._secret, message.encode('utf-8'), hashlib.sha256).hexdigest()

    @staticmethod
    def normalize_ticker(symbol: str) -> str:
        """Ensures uniform ticker formatting."""
        return symbol.replace('/', '').upper().strip()

def get_nonce() -> int:
    """Timestamp-based nonce for order execution."""
    return int(time.time() * 1000)

def format_crypto_amount(value: float, precision: int = 8) -> str:
    """String formatting for high precision assets."""
    return f"{value:.{precision}f}".rstrip('0').rstrip('.')

class ResponseParser:
    @classmethod
    def extract_price(cls, raw_data: Dict[str, Any]) -> float:
        """Extraction logic for nested ticker responses."""
        try:
            return float(raw_data.get('lastPrice') or raw_data.get('close', 0))
        except (ValueError, TypeError):
            return 0.0