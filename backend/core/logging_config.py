import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    log_path = Path("./logs/corevalora.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5),
                            logging.StreamHandler(),
                        ])
