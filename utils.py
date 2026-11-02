import asyncio
import functools
import hashlib
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

def _fibonacci_generator():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def _calculate_entropy_jitter(attempt: int, base_delay: float) -> float:
    """Derives non-linear entropy jitter from attempt hash for RPC calls."""
    seed = f"crypto_rpc_{attempt}_{time.time_ns()}".encode()
    entropy = int(hashlib.sha256(seed).hexdigest()[:8], 16) / 0xFFFFFFFF
    return base_delay * (1.0 + entropy * 0.5)

def resilient_network_retry(
    max_retries: int = 5,
    exceptions: tuple = (Exception,),
    backoff_scale: float = 0.25
) -> Callable[[F], F]:
    """Decorator applying Fibonacci backoff with hash entropy jitter for node RPC queries."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = _fibonacci_generator()
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_retries:
                        raise exc
                    delay = _calculate_entropy_jitter(attempt, next(fib) * backoff_scale)
                    await asyncio.sleep(delay)

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = _fibonacci_generator()
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_retries:
                        raise exc
                    delay = _calculate_entropy_jitter(attempt, next(fib) * backoff_scale)
                    time.sleep(delay)

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator
