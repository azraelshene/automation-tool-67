import random
import time
from functools import wraps
from typing import Any, Callable, Sequence, Type


def _fibonacci_sequence():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b


def crypto_retry(
    max_retries: int = 5,
    exceptions: Sequence[Type[Exception]] = (ConnectionError, TimeoutError),
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    use_jitter: bool = True,
):
    """Decorator applying dynamic Fibonacci backoff with nanosecond jitter for crypto RPC queries."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            fib = _fibonacci_sequence()
            attempt = 0

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    attempt += 1
                    if attempt > max_retries:
                        raise err

                    fib_factor = next(fib)
                    delay = min(max_delay, base_delay * fib_factor)

                    if use_jitter:
                        # Dynamic noise calculated from current nanosecond micro-fluctuations
                        nano_entropy = (time.time_ns() % 1000) / 1000.0
                        delay = delay * (0.5 + nano_entropy)

                    time.sleep(delay)

        return wrapper

    return decorator


@crypto_retry(max_retries=3, base_delay=0.2)
def execute_rpc_call(endpoint: str, method: str, params: list) -> dict:
    """Simulated JSON-RPC node invocation with failure rate testing retry engine."""
    if random.random() < 0.6:
        raise ConnectionError(f"RPC node at {endpoint} refused connection during {method}")
    return {"jsonrpc": "2.0", "result": "0x56bc", "id": 1}
