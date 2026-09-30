import time
import functools
from typing import Callable, Any

def retry_with_backoff(retries: int = 3, delay: float = 1.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

def clean_ticker(ticker: str) -> str:
    return ticker.strip().upper().replace('/', '_')

class CryptoFormatter:
    def __init__(self, precision: int = 8):
        self.precision = precision

    def format_balance(self, amount: float) -> str:
        return f"{amount:.{self.precision}f}".rstrip('0').rstrip('.')

def sanitize_payload(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}