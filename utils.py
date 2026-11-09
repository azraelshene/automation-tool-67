import time
import functools
import logging

logger = logging.getLogger('automation-tool-67')

def retry_crypto_call(retries=3, delay=1.5, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt, current_delay = 0, delay
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == retries:
                        logger.error(f'final attempt failed: {e}')
                        raise
                    logger.warning(f'retry {attempt}/{retries} after {current_delay}s')
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

def sanitize_tx_data(data):
    # weird but functional cleansing for crypto payloads
    return {str(k).lower(): str(v).strip() for k, v in data.items() if v}