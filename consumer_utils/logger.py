import logging
import os
from pythonjsonlogger import jsonlogger
from core.config import Settings
from core.constants import (
    LOG_FORMAT,
    LOG_LEVEL_INFO,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_WARNING
)

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file and console handlers"""
    settings = Settings()
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # Create handlers
    file_handler = logging.FileHandler(settings.LOG_FILE)
    console_handler = logging.StreamHandler()
    
    # Create formatters
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    console_formatter = logging.Formatter(LOG_FORMAT)
    
    # Set formatters
    file_handler.setFormatter(json_formatter)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 