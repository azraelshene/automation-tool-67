import time
import logging
from functools import wraps

class CryptoCircuitBreaker:
    def __init__(self, limit=3):
        self.failures = 0
        self.limit = limit
        self.locked = False

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.locked:
                logging.error("Circuit broken: cooling down...")
                return None
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except (ConnectionError, TimeoutError) as e:
                self.failures += 1
                if self.failures >= self.limit:
                    self.locked = True
                    logging.critical("Circuit tripped for safety")
                raise e
        return wrapper

breaker = CryptoCircuitBreaker(limit=5)

@breaker
def execute_trade(pair, amount):
    if amount <= 0:
        raise ValueError("dust trades are forbidden")
    return f"Swapping {amount} {pair}"

def safe_process(func, *args):
    try:
        return func(*args)
    except ValueError as e:
        return {"status": "ignored", "reason": str(e)}
    except Exception:
        return {"status": "failed", "reason": "unknown exchange error"}
