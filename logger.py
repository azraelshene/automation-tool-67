import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class CryptoFormatter(logging.Formatter):
    """Custom formatter injecting crypto-themed indicators and dynamic tags."""

    LEVEL_EMOJIS = {
        logging.DEBUG: "🔍",
        logging.INFO: "⚡",
        logging.WARNING: "⚠️",
        logging.ERROR: "🚨",
        logging.CRITICAL: "💀",
    }

    def format(self, record: logging.LogRecord) -> str:
        emoji = self.LEVEL_EMOJIS.get(record.levelno, "📌")
        record.crypto_prefix = f"[{emoji} {record.levelname}]"
        return super().format(record)


def setup_logger(
    name: str = "automation_67",
    log_dir: str = "logs",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 7,
) -> logging.Logger:
    """Configures a logger with size-based rotation and crypto-styled formatting."""
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    log_file = path / f"{name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    fmt = "%(asctime)s | %(crypto_prefix)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    formatter = CryptoFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


bot_logger = setup_logger()
