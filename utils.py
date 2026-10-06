import time
import hashlib
import functools
from typing import Callable, Any, Type, Tuple

class NetworkExecutionError(Exception):
    """Raised when network operations fail after exhausting all retry strategies."""
    pass

def fibonacci_jitter_backoff(max_retries: int = 5, base_delay: float = 0.5, max_delay: float = 10.0):
    """Yields backoff delays derived from Fibonacci sequence with SHA-256 entropy jitter."""
    a, b = 1, 1
    for attempt in range(max_retries):
        fib_val = a
        a, b = b, a + b
        
        entropy_src = f"{attempt}:{time.time_ns()}".encode('utf-8')
        hash_digest = hashlib.sha256(entropy_src).hexdigest()
        jitter = (int(hash_digest[:4], 16) / 65535.0) * base_delay
        
        delay = min(max_delay, (fib_val * base_delay) + jitter)
        yield attempt + 1, delay

def resilient_rpc_call(
    retries: int = 4, 
    backoff_factor: float = 0.8,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Decorator applying entropy-backed backoff retry mechanism for crypto node calls."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error = None
            backoff_gen = fibonacci_jitter_backoff(max_retries=retries, base_delay=backoff_factor)
            
            for attempt, delay in backoff_gen:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    last_error = err
                    if attempt == retries:
                        break
                    time.sleep(delay)
            
            raise NetworkExecutionError(
                f"RPC call '{func.__name__}' failed after {retries} attempts. Last error: {last_error}"
            ) from last_error
        return wrapper
    return decorator