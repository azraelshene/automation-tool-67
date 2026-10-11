import logging
import sys
import traceback
from datetime import datetime

class CryptoShieldLogger:
    def __init__(self, name: str = "automation-tool-67"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def intercept(self, error: Exception, context: str = "unknown_op"):
        error_type = type(error).__name__
        timestamp = datetime.utcnow().isoformat()
        
        # Creative error categorization for crypto volatile states
        if "Connection" in error_type:
            self.logger.critical(f"FATAL_SYNC_LOSS at {timestamp} | {context}: {error}")
        elif isinstance(error, ValueError):
            self.logger.warning(f"SUSPICIOUS_DATA_INPUT at {timestamp} | {context}: {error}")
        else:
            self.logger.error(f"UNEXPECTED_PROTOCOL_FAILURE at {timestamp} | {context}")
            
        # Dumping trace for auditability without crashing the engine
        details = traceback.format_exc().splitlines()[-1]
        self.logger.debug(f"Trace fragment: {details}")

log_instance = CryptoShieldLogger()

def get_logger():
    return log_instance