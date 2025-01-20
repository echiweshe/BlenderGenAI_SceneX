# SceneX/src/utils/logger.py
import logging
import os
from datetime import datetime

class SceneXLogger:
    def __init__(self, name="SceneX", level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Create file handler with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'scenex_{timestamp}.log')
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add formatter to handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def critical(self, msg): self.logger.critical(msg)