import json
import random
import time
import urllib.error
import urllib.request
from functools import wraps
from typing import Any, Callable, Tuple, Type


class CryptoNetworkError(Exception):
    """Raised when a crypto API or RPC node fails permanently."""
    pass


def _fibonacci_sequence():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def adaptive_retry(
    max_attempts: int = 5,
    backoff_multiplier: float = 0.5,
    retryable_exceptions: Tuple[Type[Exception], ...] = (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
    ),
):
    """Decorator implementing fibonacci backoff with entropy jitter for crypto RPC/REST calls."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = _fibonacci_sequence()
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as err:
                    last_exception = err
                    if attempt == max_attempts:
                        break
                    
                    base_delay = next(fib) * backoff_multiplier
                    jitter = random.uniform(0.1, 0.4) * base_delay
                    sleep_time = round(base_delay + jitter, 3)
                    time.sleep(sleep_time)
            
            raise CryptoNetworkError(
                f"Network operation {func.__name__} failed after {max_attempts} retries. Cause: {last_exception}"
            )
        return wrapper
    return decorator


@adaptive_retry(max_attempts=4, backoff_multiplier=0.2)
def fetch_crypto_price(symbol: str = "BTCUSDT") -> dict:
    """Fetch ticker information from Binance public endpoint with automated retry."""
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    req = urllib.request.Request(url, headers={"User-Agent": "automation-tool-67/1.0"})
    with urllib.request.urlopen(req, timeout=5) as response:
        if response.status == 200:
            data = json.loads(response.read().decode("utf-8"))
            return {"symbol": data.get("symbol"), "price": float(data.get("price", 0.0))}
    raise urllib.error.URLError("Failed to fetch valid price payload")
