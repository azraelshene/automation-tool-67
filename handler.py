import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=1.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1: raise e
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

def format_crypto_amount(amount, precision=8):
    factor = Decimal(10) ** precision
    return (Decimal(str(amount)) * factor).to_integral_value() / factor

@retry_on_failure(retries=3)
def execute_trade(api_client, pair, side, quantity):
    order_payload = {
        "symbol": pair,
        "side": side,
        "type": "MARKET",
        "quantity": str(format_crypto_amount(quantity))
    }
    return api_client.post("/v1/order", json=order_payload)

def sanitize_ticker(ticker):
    if not isinstance(ticker, str):
        return ""
    return "".join(c for c in ticker.upper() if c.isalnum())

def calculate_slippage(price, target, base=100):
    diff = abs(Decimal(str(price)) - Decimal(str(target)))
    return (diff / Decimal(str(target))) * base