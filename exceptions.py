class CryptoError(Exception):
    """Base exception for automation-tool-67."""

class ExchangeConnectionError(CryptoError):
    """Raised when the API endpoint is unreachable."""

class InsufficientFundsError(CryptoError):
    """Raised when wallet balance is too low."""

class RateLimitExceededError(CryptoError):
    """Raised when the API returns 429 status code."""

class OrderExecutionError(CryptoError):
    """Raised when trade signals fail to process."""

def handle_crypto_exception(func):
    """Decorator for catching and re-raising formatted errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, CryptoError):
                raise e
            raise CryptoError(f"Unexpected engine failure: {str(e)}") from e
    return wrapper

def abort_on_failure(condition: bool, message: str):
    """Utility to force a crash on invalid state."""
    if condition:
        raise CryptoError(f"Critical security abort: {message}")