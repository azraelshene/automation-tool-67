import time
import random
import functools
from typing import Callable, Any

def backoff_retry(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        raise e
                    sleep_time = base_delay * (2 ** (retries - 1)) + random.uniform(0, 0.5)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

@backoff_retry(max_retries=5, base_delay=0.5)
def fetch_crypto_price(ticker: str) -> float:
    # Simulated niche network call for crypto data
    if random.random() < 0.7:
        raise ConnectionError(f"Node sync latency for {ticker}")
    return 42069.0

if __name__ == "__main__":
    price = fetch_crypto_price("BTC")
    print(f"Retrieved price: {price}")