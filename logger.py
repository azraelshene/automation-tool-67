import logging
import os
from logging.handlers import RotatingFileHandler

def get_crypto_logger(name: str = 'automation-tool-67') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, 'blockchain.log')
        
        # 5MB per file, keep 3 backups
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        
        # custom format for easier grepping of wallet tx logs
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # console fallback for non-daemonized runs
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        
        logger.addHandler(handler)
        logger.addHandler(console)
        
    return logger