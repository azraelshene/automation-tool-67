import time
import logging
from functools import wraps

logger = logging.getLogger('crypto-bot')

class CryptoError(Exception):
    pass

def fault_tolerant_execution(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    logger.warning(f"network instability, retry {attempts}/{max_retries}")
                    time.sleep(2 ** attempts)
                except Exception as e:
                    logger.error(f"fatal trade breach: {str(e)}")
                    raise CryptoError("unrecoverable market state") from e
            raise CryptoError("exhausted retry attempts")
        return wrapper
    return decorator

@fault_tolerant_execution(max_retries=5)
def execute_trade(pair, amount):
    if amount <= 0:
        raise ValueError("dust trade detected")
    # Simulate market execution
    logger.info(f"executing {amount} on {pair}")
    return True