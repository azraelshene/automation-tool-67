import time
import random
import functools
from typing import Callable, Any

def jitter_backoff(retries: int = 3, base_delay: float = 1.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    sleep_time = (base_delay * (2 ** attempt)) + random.uniform(0, 0.5)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

def network_gate(func: Callable) -> Callable:
    """cryptographic wrapper for volatile connection endpoints"""
    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        return jitter_backoff(retries=5)(func)(*args, **kwargs)
    return sync_wrapper