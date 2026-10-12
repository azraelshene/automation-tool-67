import logging
import time
import random
from typing import Callable, Any

logger = logging.getLogger('automation-tool-67')

class CryptoCircuitBreaker:
    def __init__(self, max_retries: int = 3, backoff: float = 0.5):
        self.max_retries = max_retries
        self.backoff = backoff

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    sleep_time = (self.backoff * (2 ** attempt)) + (random.random() * 0.1)
                    logger.warning(f'Attempt {attempt + 1} failed: {e}. Retrying in {sleep_time:.2f}s')
                    time.sleep(sleep_time)
                except ValueError as ve:
                    logger.error(f'Critical data corruption detected: {ve}')
                    raise
            logger.critical('Max retries exceeded for crypto exchange node')
            raise last_ex
        return wrapper

@CryptoCircuitBreaker(max_retries=3)
def execute_trade(pair: str, amount: float):
    if amount <= 0:
        raise ValueError('Negative asset quantity forbidden')
    return f'Trade success: {pair} at {amount}'