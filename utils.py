import random
import time
from functools import wraps
from typing import Callable, Any, Tuple, Type

class CryptoNetworkError(Exception):
    """Raised when a crypto RPC or Web3 endpoint fails all retry attempts."""
    pass

def _fibonacci_jitter_stream(initial: float = 0.5, max_delay: float = 30.0):
    """Yields fibonacci-based delay intervals with randomized jitter for crypto nodes."""
    a, b = initial, initial
    while True:
        jitter = random.uniform(-0.1, 0.25) * a
        yield min(max_delay, max(0.05, a + jitter))
        a, b = b, a + b

def resilient_rpc_call(
    max_attempts: int = 5,
    catches: Tuple[Type[Exception], ...] = (Exception,),
    backoff_base: float = 0.4
):
    """Decorator injecting fibonacci backoff retry logic into crypto network requests."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay_generator = _fibonacci_jitter_stream(backoff_base)
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except catches as err:
                    last_exception = err
                    if attempt == max_attempts:
                        break
                    wait_time = next(delay_generator)
                    time.sleep(wait_time)

            raise CryptoNetworkError(
                f"Endpoint execution '{func.__name__}' failed after {max_attempts} retries: {last_exception}"
            ) from last_exception
        return wrapper
    return decorator

def execute_with_fallback(primary_fn: Callable, fallback_fn: Callable, *args, **kwargs) -> Any:
    """Executes primary endpoint with retry logic, failing over to backup RPC on exhaust."""
    try:
        return resilient_rpc_call(max_attempts=3)(primary_fn)(*args, **kwargs)
    except CryptoNetworkError:
        return resilient_rpc_call(max_attempts=3)(fallback_fn)(*args, **kwargs)
