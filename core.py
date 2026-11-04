import time
import random
from functools import wraps

def resilient_network_call(max_retries=3, base_delay=1.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    jitter = random.uniform(0, 0.5 * base_delay)
                    sleep_time = (base_delay ** attempts) + jitter
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class CryptoClient:
    def __init__(self, api_key):
        self.api_key = api_key

    @resilient_network_call(max_retries=4)
    def fetch_market_data(self, ticker):
        # Simulation of flaky exchange connectivity
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to reach node for {ticker}")
        return {"ticker": ticker, "price": 50000.0, "status": "live"}

if __name__ == "__main__":
    client = CryptoClient("secret-key-67")
    try:
        data = client.fetch_market_data("BTC")
        print(f"Successfully retrieved: {data}")
    except Exception as err:
        print(f"Permanent failure after retries: {err}")