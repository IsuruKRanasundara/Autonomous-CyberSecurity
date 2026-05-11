"""Centralized logging configuration for the application."""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from app.config.settings import settings


# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output."""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
            )
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """Get or create a logger with the configured handlers.

    Args:
        name: Logger name (typically __name__).

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.logging.LOG_LEVEL))

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.logging.LOG_LEVEL))
        console_formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler (if configured)
        if settings.logging.LOG_FILE:
            file_path = Path(settings.logging.LOG_FILE)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.handlers.RotatingFileHandler(
                file_path,
                maxBytes=10 * 1024 * 1024,  # 10 MB
                backupCount=5,
            )
            file_handler.setLevel(getattr(logging, settings.logging.LOG_LEVEL))
            file_formatter = logging.Formatter(settings.logging.LOG_FORMAT)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    return logger


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> None:
    """Configure root logger and all loggers.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Path to log file.
        log_format: Log format string.
    """
    log_level = level or settings.logging.LOG_LEVEL
    file_path = log_file or settings.logging.LOG_FILE
    fmt = log_format or settings.logging.LOG_FORMAT

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))
    console_formatter = ColoredFormatter(fmt)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler
    if file_path:
        log_file_path = Path(file_path)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
        )
        file_handler.setLevel(getattr(logging, log_level))
        file_formatter = logging.Formatter(fmt)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Silence noisy third-party libraries
    logging.getLogger("kafka").setLevel(logging.WARNING)
    logging.getLogger("elasticsearch").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    root_logger.info(
        "Logging configured: level=%s, file=%s",
        log_level,
        file_path or "none",
    )


def get_app_logger() -> logging.Logger:
    """Get the application logger.

    Returns:
        Logger instance for the app module.
    """
    return get_logger("app")


def get_agent_logger() -> logging.Logger:
    """Get the agents logger.

    Returns:
        Logger instance for the agents module.
    """
    return get_logger("app.agents")


def get_api_logger() -> logging.Logger:
    """Get the API logger.

    Returns:
        Logger instance for the API module.
    """
    return get_logger("app.api")


def get_ingestion_logger() -> logging.Logger:
    """Get the ingestion logger.

    Returns:
        Logger instance for the ingestion module.
    """
    return get_logger("app.ingestion")


def get_storage_logger() -> logging.Logger:
    """Get the storage logger.

    Returns:
        Logger instance for the storage module.
    """
    return get_logger("app.storage")


def get_ai_logger() -> logging.Logger:
    """Get the AI/LLM logger.

    Returns:
        Logger instance for the AI module.
    """
    return get_logger("app.ai")
