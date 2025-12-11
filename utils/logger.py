import logging
import logging.handlers
from config.settings import SETTINGS
import os

def setup_logging():
    """Настройка логирования"""
    
    # Направляющие
    log_level = getattr(logging, SETTINGS.LOG_LEVEL, logging.INFO)
    
    # Консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Файл
    os.makedirs('logs', exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        SETTINGS.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Настройка root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger
