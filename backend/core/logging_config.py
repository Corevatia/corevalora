import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            RotatingFileHandler("./logs/corevalora.log", maxBytes=5 * 1024 * 1024, backupCount=5),
                            logging.StreamHandler(),
                        ])
