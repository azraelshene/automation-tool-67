import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = 'automation-tool-67') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [wallet-op] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_path = os.path.join(log_dir, 'crypto_trace.log')
    
    # 5MB rotation, keeps 3 history files
    handler = RotatingFileHandler(
        file_path, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console)

    return logger

# Initialize global logger instance
crypto_logger = get_crypto_logger()