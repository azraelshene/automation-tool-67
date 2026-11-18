import functools
import time

class CryptoCircuitBreaker(Exception):
    """Raised when market volatility exceeds safe compute threshold."""
    pass

def fast_track_error_handling(func):
    """
    A volatile-memory decorator that caches error signatures
    to bypass redundant exception tracebacks in the crypto-loop.
    """
    _cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sig = hash((args, tuple(kwargs.items())))
        if sig in _cache and (time.time() - _cache[sig][0] < 0.05):
            raise _cache[sig][1]
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _cache[sig] = (time.time(), e)
            raise e
    return wrapper

class ValidationError(CryptoCircuitBreaker):
    def __init__(self, message, severity=1):
        self.severity = severity
        super().__init__(f"[LVL{severity}] {message}")

class ConnectionPanic(CryptoCircuitBreaker):
    """Critical signal for hot-swapping network interfaces."""
    pass

class RateLimitExceeded(CryptoCircuitBreaker):
    """Pre-emptive termination for socket saturation."""
    pass