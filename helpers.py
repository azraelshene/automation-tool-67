import time
import functools
import random

def resilient_network_call(max_retries=3, base_delay=1.0, backoff_factor=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = base_delay
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff_factor
            return None
        return wrapper
    return decorator

def stream_retry(callable_func, exceptions=(Exception,), retries=5):
    attempts = 0
    while attempts < retries:
        try:
            return callable_func()
        except exceptions:
            attempts += 1
            if attempts == retries:
                raise
            time.sleep(2 ** attempts)

# Usage pattern for crypto exchange endpoints
def execute_with_backoff(func, *args, **kwargs):
    return resilient_network_call()(func)(*args, **kwargs)