import time
from typing import Callable, Any, Generator, List

class CryptoUnitConverter:
    """Dynamically converts Wei to Gwei, Eth, and other units using attribute routing."""
    UNITS = {
        "wei": 1,
        "kwei": 10**3,
        "mwei": 10**6,
        "gwei": 10**9,
        "szabo": 10**12,
        "finney": 10**15,
        "ether": 10**18
    }

    def __init__(self, value_in_wei: int):
        self._wei = int(value_in_wei)

    def __getattr__(self, name: str) -> float:
        clean_name = name.lower()
        if clean_name in self.UNITS:
            return self._wei / self.UNITS[clean_name]
        raise AttributeError(f"Unknown Ethereum unit: {name}")

def chunk_payloads(items: List[Any], batch_size: int) -> Generator[List[Any], None, None]:
    """Yields successive batches of items for bulk RPC processing."""
    if batch_size <= 0:
        raise ValueError("Batch size must be greater than zero")
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def retry_on_transient_error(retries: int = 3, backoff: float = 1.5):
    """Decorator to retry flaky node requests using a dynamic backoff coefficient."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = 1.0
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    if attempt == retries - 1:
                        raise err
                    time.sleep(delay)
                    delay *= backoff
        return wrapper
    return decorator