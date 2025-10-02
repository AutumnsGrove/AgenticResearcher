"""
Logging Configuration

This module sets up structured logging for the agentic research system.
It provides consistent logging format with timestamps, levels, and component names.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to log levels for terminal output.
    """

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }

    def format(self, record):
        """Format log record with colors."""
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        return super().format(record)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    component: Optional[str] = None,
    use_colors: bool = True
) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging output
        component: Optional component name for namespaced logging
        use_colors: Whether to use colored output (default: True)

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logging(level="DEBUG", component="orchestrator")
        >>> logger.info("Starting research")
        [2025-10-02 14:30:15] [INFO] [orchestrator] Starting research
    """
    # Create logger
    logger_name = f"agentic_research.{component}" if component else "agentic_research"
    logger = logging.getLogger(logger_name)

    # Set level
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    logger.setLevel(numeric_level)

    # Remove existing handlers
    logger.handlers = []

    # Create formatters
    log_format = "[%(asctime)s] [%(levelname)s]"
    if component:
        log_format += f" [{component}]"
    log_format += " %(message)s"

    date_format = "%Y-%m-%d %H:%M:%S"

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)

    if use_colors and sys.stdout.isatty():
        console_formatter = ColoredFormatter(log_format, datefmt=date_format)
    else:
        console_formatter = logging.Formatter(log_format, datefmt=date_format)

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_formatter = logging.Formatter(log_format, datefmt=date_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(component: str) -> logging.Logger:
    """
    Get a logger for a specific component.

    Args:
        component: Component name (e.g., "orchestrator", "search_agent")

    Returns:
        Logger instance for the component

    Example:
        >>> logger = get_logger("compression_agent")
        >>> logger.debug("Compressing search results")
    """
    return logging.getLogger(f"agentic_research.{component}")


def set_global_level(level: str) -> None:
    """
    Set the logging level for all loggers.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    # Set level for root logger
    root_logger = logging.getLogger("agentic_research")
    root_logger.setLevel(numeric_level)

    # Update all handlers
    for handler in root_logger.handlers:
        handler.setLevel(numeric_level)


def configure_production_logging(log_dir: str = "logs") -> None:
    """
    Configure logging for production environment.

    Sets up:
    - INFO level for console
    - DEBUG level for file
    - Separate error log file
    - Log rotation

    Args:
        log_dir: Directory for log files
    """
    from logging.handlers import RotatingFileHandler

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Root logger
    root_logger = logging.getLogger("agentic_research")
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = []

    # Console handler (INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = ColoredFormatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Main log file (DEBUG level, rotating)
    main_log_file = log_path / "agentic_research.log"
    main_handler = RotatingFileHandler(
        main_log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    main_handler.setLevel(logging.DEBUG)
    main_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    main_handler.setFormatter(main_formatter)
    root_logger.addHandler(main_handler)

    # Error log file (ERROR level, rotating)
    error_log_file = log_path / "errors.log"
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    error_handler.setFormatter(error_formatter)
    root_logger.addHandler(error_handler)

    root_logger.info("Production logging configured")


def configure_debug_logging() -> None:
    """
    Configure logging for debug/development environment.

    Sets DEBUG level everywhere with verbose output.
    """
    root_logger = logging.getLogger("agentic_research")
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers = []

    # Console handler with verbose format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = ColoredFormatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    root_logger.debug("Debug logging configured")
