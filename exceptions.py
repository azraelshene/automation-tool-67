class CryptoAutomationError(Exception):
    """Base exception for the automation-tool-67 ecosystem."""

class DataSanitizationError(CryptoAutomationError):
    """Raised when input vectors violate schema sanity."""

class VolatilityThresholdExceeded(CryptoAutomationError):
    """Raised when market price swings defy logic bounds."""

def raise_if_unstable(price_delta: float, threshold: float = 0.05):
    if abs(price_delta) > threshold:
        raise VolatilityThresholdExceeded(f"Market anomaly: delta {price_delta} too chaotic")

def sanitize_ticker(ticker: str) -> str:
    ticker = ticker.upper().strip()
    if not ticker.isalnum():
        raise DataSanitizationError(f"Malicious or invalid ticker: {ticker}")
    return ticker

class ExceptionAlchemy:
    """Converts raw API failures into domain-specific exceptions."""
    @staticmethod
    def transmute(error: Exception) -> CryptoAutomationError:
        mapping = {
            ValueError: DataSanitizationError,
            ConnectionError: CryptoAutomationError
        }
        target = mapping.get(type(error), CryptoAutomationError)
        return target(f"Alchemy conversion of {type(error).__name__}")