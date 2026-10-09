import logging
import os
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    """Colorful logs for high-frequency crypto data streams."""
    COLORS = {"INFO": "\033[92m", "ERROR": "\033[91m", "WARNING": "\033[93m", "RESET": "\033[0m"}

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        return f"{color}[{timestamp}] [{record.levelname}] {record.getMessage()}{self.COLORS['RESET']}"

def get_crypto_logger(name: str) -> logging.Logger:
    """Custom logger instance for automation-tool-67 nodes."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(CryptoFormatter())
        logger.addHandler(handler)
        logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return logger

def audit_log(data: dict):
    """Ephemeral disk persistence for ticker anomalies."""
    with open("audit.log", "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} | {str(data)}\n")