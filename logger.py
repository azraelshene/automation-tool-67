import logging
from logging.handlers import RotatingFileHandler
import os

def get_crypto_logger(name='automation-tool-67', log_file='crypto_engine.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # ensure log dir exists
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_path = os.path.join(log_dir, log_file)
    
    # unique rotating file handler for 5MB logs
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    
    # custom crypto-themed format
    formatter = logging.Formatter(
        '[%(asctime)s] ₿ | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # add stream handler for console visibility
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# global logger instance
log = get_crypto_logger()