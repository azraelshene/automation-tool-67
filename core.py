import time
import random
from functools import wraps

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while x < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    sleep_time = (backoff_in_seconds * (2 ** x)) + random.uniform(0, 1)
                    print(f"Network glitch: {e}. Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                    x += 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_with_backoff(retries=5, backoff_in_seconds=2)
def fetch_price_data(ticker):
    """Simulates a volatile network request to exchange API"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Exchange node unresponsive")
    return {"ticker": ticker, "price": random.uniform(1000, 60000)}