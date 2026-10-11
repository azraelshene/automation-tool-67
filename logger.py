import os
import logging
from logging.handlers import TimedRotatingFileHandler

class CryptoFormatter(logging.Formatter):
    EMOJIS = {
        logging.DEBUG: "🔍 [TRACE]",
        logging.INFO: "⚡ [TRADE]",
        logging.WARNING: "⚠️ [VOLATILE]",
        logging.ERROR: "🚨 [SLIPPAGE]",
        logging.CRITICAL: "💥 [LIQUIDATED]"
    }

    def format(self, record):
        record.crypto_tag = self.EMOJIS.get(record.levelno, "🌐 [MARKET]")
        return super().format(record)

def setup_crypto_logger(name: str = "bot_core", log_dir: str = "logs") -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_path = os.path.join(log_dir, f"{name}.log")
    fmt = "%(asctime)s | %(crypto_tag)s | %(threadName)s | %(message)s"
    formatter = CryptoFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    handler = TimedRotatingFileHandler(
        log_path, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger

if __name__ == "__main__":
    log = setup_crypto_logger()
    log.info("Engine booted, watching BTC/USDT pair")
    log.warning("High gas fees detected on mainnet")
    log.error("Order execution failed: orderbook spread too wide")