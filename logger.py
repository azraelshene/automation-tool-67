import logging
import json
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "ts": datetime.utcnow().isoformat(),
            "lvl": record.levelname,
            "msg": record.getMessage(),
            "tool": "automation-tool-67"
        }
        if hasattr(record, 'tx_hash'):
            log_entry['tx'] = record.tx_hash
        return json.dumps(log_entry)

def get_crypto_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(CryptoFormatter())
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def log_trade(logger, pair: str, amount: float, tx_hash: str):
    extra = {'tx_hash': tx_hash}
    logger.info(f"trade execution: {pair} amount {amount}", extra=extra)

# usage example: logger = get_crypto_logger("bot")
# log_trade(logger, "BTC/USDT", 0.05, "0xabc123")