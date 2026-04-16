"""
Logger module for tracking user interactions and debugging.
"""
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import colorlog


class JarvisLogger:
    """Custom logger for Jarvis AI Assistant."""
    
    def __init__(self, name: str = "jarvis", log_file: Optional[str] = None, level: str = "INFO"):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            log_file: Path to log file (optional)
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Console handler with colors
        console_handler = colorlog.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if log file specified)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(message, **kwargs)
    
    def log_user_interaction(self, query: str, response: str, response_time: float):
        """
        Log user interaction for analytics.
        
        Args:
            query: User query
            response: Assistant response
            response_time: Time taken to generate response (seconds)
        """
        self.info(
            f"User Interaction - Query: '{query[:100]}...' | "
            f"Response Time: {response_time:.2f}s | "
            f"Response Length: {len(response)} chars"
        )


def get_logger(name: str = "jarvis", log_file: Optional[str] = None, level: str = "INFO") -> JarvisLogger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level
    
    Returns:
        JarvisLogger instance
    """
    return JarvisLogger(name=name, log_file=log_file, level=level)
