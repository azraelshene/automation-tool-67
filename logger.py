import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = "automation-tool-67"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        file_path = os.path.join(log_dir, "crypto_ops.log")
        handler = RotatingFileHandler(
            file_path, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

logger = get_crypto_logger()