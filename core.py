import time
import random
import functools
from typing import Callable, Any

def retry_request(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    jitter = random.uniform(0, 0.5)
                    sleep_time = (base_delay * (2 ** (attempts - 1))) + jitter
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@retry_request(max_retries=5, base_delay=0.5)
def fetch_price_data(ticker: str) -> dict:
    # Simulate volatile crypto network behavior
    if random.random() < 0.7:
        raise ConnectionError("Market API timeout")
    return {"symbol": ticker, "price": random.uniform(100, 50000)}

if __name__ == "__main__":
    try:
        data = fetch_price_data("BTC")
        print(f"Successfully retrieved: {data}")
    except Exception as e:
        print(f"Final failure after retries: {e}")