from __future__ import annotations

import logging.config

from colorlog import ColoredFormatter


class LogConfig:
    """Centralized configuration for logging settings."""

    LOG_COLORS = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
    COLORED_FORMAT = (
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


formatter_config = {
    "colored": {
        "()": ColoredFormatter,
        "format": LogConfig.COLORED_FORMAT,
        "datefmt": LogConfig.DATE_FORMAT,
        "log_colors": LogConfig.LOG_COLORS,
    },
    "standard": {
        "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        "datefmt": LogConfig.DATE_FORMAT,
    },
}


def configure_logging() -> None:
    """Configure logging for the whole project."""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": formatter_config,
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "colored",
            },
        },
        # No need to define individual loggers unless you want special settings
        "root": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    }
    logging.config.dictConfig(logging_config)
