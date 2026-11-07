import time
import hashlib
from typing import Any, Callable

def retry_on_failure(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def generate_crypto_id(payload: str) -> str:
    return hashlib.sha256(f'{payload}{time.time_ns()}'.encode()).hexdigest()[:16]

def sanitize_float(value: Any) -> float:
    try:
        return float(str(value).replace(',', '.'))
    except (ValueError, TypeError):
        return 0.0

def format_currency(amount: float, precision: int = 8) -> str:
    return f'{amount:.{precision}f}'.rstrip('0').rstrip('.') or '0'