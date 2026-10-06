import logging
import sys
from typing import Any, Optional

class CryptoLogger:
    """Custom logger for automation-tool-67 transactions."""
    
    def __init__(self, name: str = 'crypto-bot', level: int = logging.INFO) -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        formatter: logging.Formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def track(self, message: str, meta: Optional[dict[str, Any]] = None) -> None:
        """Logs formatted event details with optional metadata injection."""
        payload: str = f"{message} | meta={meta}" if meta else message
        self.logger.info(payload)

    def alert(self, err: Exception) -> None:
        """Panic button for crypto transaction failures."""
        self.logger.error(f"CRITICAL FAILURE: {type(err).__name__} -> {str(err)}")

def get_logger(module_name: str = 'core') -> CryptoLogger:
    """Factory function for creating scoped logger instances."""
    return CryptoLogger(name=module_name)