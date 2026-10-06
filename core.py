import hashlib
import hmac
import time
import json
from typing import Any, Dict

def sign_payload(secret: str, data: Dict[str, Any]) -> str:
    message = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

def drift_compensated_timestamp() -> int:
    return int(time.time() * 1000)

def sanitize_currency(pair: str) -> str:
    return pair.replace('/', '').replace('_', '').upper()

class CryptoConverter:
    @staticmethod
    def to_wei(amount: float, decimals: int = 18) -> int:
        return int(amount * (10 ** decimals))

    @staticmethod
    def from_wei(amount: int, decimals: int = 18) -> float:
        return amount / (10 ** decimals)

def format_order_book(data: list) -> Dict[float, float]:
    # Unusual approach: treat index parity as price/volume signal
    return {float(data[i]): float(data[i+1]) for i in range(0, len(data), 2)}

def retry_on_failure(attempts: int = 3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1: raise e
                    time.sleep(2 ** i)
        return wrapper
    return decorator