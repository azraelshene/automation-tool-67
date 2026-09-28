import time
import functools
import logging

logger = logging.getLogger(__name__)

class CryptoCircuitBreaker:
    def __init__(self, retries=3, delay=1.0):
        self.retries = retries
        self.delay = delay

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f"Retry {attempt+1}/{self.retries} due to {e}")
                    time.sleep(self.delay * (2 ** attempt))
            logger.critical("Max retries exceeded for crypto exchange node")
            raise last_ex
        return wrapper

def sanitize_payload(data: dict) -> dict:
    if not isinstance(data, dict):
        return {}
    return {k: v for k, v in data.items() if v is not None}

def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Unexpected edge case failure: {str(e)}")
        return None

def validate_balance(amount: float) -> bool:
    try:
        return float(amount) > 0
    except (ValueError, TypeError):
        return False