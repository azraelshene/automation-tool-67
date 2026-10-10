import hashlib
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict


class CryptoBlockFormatter(logging.Formatter):
    """Custom log formatter that attaches a hash signature to every log record."""

    def __init__(self, key_id: str = "node-01"):
        super().__init__()
        self.key_id = key_id
        self._prev_hash = "0" * 32

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "node": self.key_id,
            "prev_hash": self._prev_hash,
        }
        
        raw_bytes = json.dumps(log_entry, sort_keys=True).encode("utf-8")
        current_hash = hashlib.sha256(raw_bytes).hexdigest()[:16]
        log_entry["hash"] = current_hash
        self._prev_hash = current_hash

        return json.dumps(log_entry)


def setup_logger(
    name: str = "automation_tool",
    log_dir: str = "logs",
    max_bytes: int = 5_000_000,
    backup_count: int = 5,
) -> logging.Logger:
    """Configures a ledger-inspired rotating file logger with SHA-256 record verification."""
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    )
    logger.addHandler(console_handler)

    file_path = path / "crypto_automation.log"
    file_handler = RotatingFileHandler(
        filename=file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(CryptoBlockFormatter())
    logger.addHandler(file_handler)

    return logger


system_logger = setup_logger()
