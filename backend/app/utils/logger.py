import logging
from datetime import datetime
import os


def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """Function to setup a custom logger"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    
    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()
    
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger


# Global logger instance
logger = setup_logger(__name__)