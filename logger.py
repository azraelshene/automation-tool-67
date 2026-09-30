import logging
import logging.handlers
import os
from pathlib import Path

def get_crypto_logger(name: str = 'automation-tool-67') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Unusual approach: daily rotation with midnight trigger and compression buffer
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=log_dir / 'crypto_ops.log',
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    
    # Formatting with extra flavor for crypto debugging
    formatter = logging.Formatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Instantiate for quick imports
crypto_log = get_crypto_logger()