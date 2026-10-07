import logging
import sys
from src.config.settings import BASE_DIR

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        fh = logging.FileHandler(BASE_DIR / 'logs' / 'pipeline.log')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
