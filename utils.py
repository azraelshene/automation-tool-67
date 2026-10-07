import time
import functools
import random
from typing import Callable, Any

class NetworkException(Exception):
    pass

def retry_operation(attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    wait = delay * (2 ** i) + random.uniform(0, 0.1)
                    time.sleep(wait)
            raise NetworkException(f'failed after {attempts} attempts') from last_ex
        return wrapper
    return decorator

@retry_operation(attempts=5)
def fetch_price_data(ticker: str):
    import random
    if random.random() < 0.7:
        raise ConnectionError('node jitter')
    return {'symbol': ticker, 'price': 50000.0}