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
        
        logs_dir = BASE_DIR / 'logs'
        logs_dir.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(logs_dir / 'pipeline.log')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger
