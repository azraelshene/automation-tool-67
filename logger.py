import logging
import sys
from typing import Any, Optional

class CryptoLogger:
    def __init__(self, name: str = "automation-tool-67") -> None:
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Configure console stream handler with color simulation."""
        stream: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        stream.setFormatter(self.formatter)
        self.logger.addHandler(stream)

    def alert(self, event: str, data: Optional[Any] = None) -> None:
        """Emit a formatted log message with crypto context."""
        context: str = f" -> {data}" if data else ""
        self.logger.info(f"[!] {event.upper()}{context}")

    def log_trade(self, pair: str, side: str, amount: float) -> None:
        """Standardized trade execution logging."""
        msg: str = f"EXECUTED: {side.upper()} {amount} of {pair}"
        self.logger.info(f"[+] {msg}")

    def error_panic(self, reason: str, exc: Optional[Exception] = None) -> None:
        """Log critical failures with traceback exposure."""
        self.logger.critical(f"[FATAL] {reason} | {exc if exc else 'N/A'}")

instance: CryptoLogger = CryptoLogger()