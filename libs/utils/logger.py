import logging
import sys
from pythonjsonlogger import jsonlogger
from apps.weather_service.core.config import settings


def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger instance.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger

    # Stream handler for console output
    handler = logging.StreamHandler(sys.stdout)

    # Select formatter based on environment
    if settings.PROJECT_NAME == "production":
        # JSON Formatter for production
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s %(request_id)s"
        )
    else:
        # Standard text formatter for debugging
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Set logging level from environment or default to INFO
    log_level = settings.LOG_LEVEL if hasattr(settings, "LOG_LEVEL") else "INFO"
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    return logger
