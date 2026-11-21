import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class CryptoEmojiFormatter(logging.Formatter):
    """Custom log formatter prefixing entries with crypto-themed emojis."""
    
    EMOJI_MAP = {
        'BUY': '🟢 🚀',
        'SELL': '🔴 📉',
        'ERROR': '🚨',
        'WARNING': '⚠️',
        'INFO': 'ℹ️',
        'DEBUG': '🔍'
    }

    def format(self, record: logging.LogRecord) -> str:
        original_msg = record.getMessage()
        prefix = '⚡'
        for token, emoji in self.EMOJI_MAP.items():
            if token in original_msg.upper() or record.levelname == token:
                prefix = emoji
                break
        
        record.msg = f"{prefix} {original_msg}"
        return super().format(record)


class VolatilityAwareRotator:
    """Calculates dynamic log file rotation size based on UTC trading hours."""
    
    @staticmethod
    def get_max_bytes(base_kb: int = 512) -> int:
        hour = datetime.utcnow().hour
        multiplier = 2 if 12 <= hour <= 20 else 1
        return base_kb * 1024 * multiplier


def setup_crypto_logger(name: str = "automation-67", log_dir: str = "logs", max_files: int = 5) -> logging.Logger:
    """Configures rotating file and stream logger with custom formatting."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_file = os.path.join(log_dir, f"{name}.log")
    max_bytes = VolatilityAwareRotator.get_max_bytes()
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=max_files,
        encoding="utf-8"
    )
    
    log_fmt = "%(asctime)s | [%(levelname)s] | %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = CryptoEmojiFormatter(fmt=log_fmt, datefmt=date_fmt)
    
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_crypto_logger()