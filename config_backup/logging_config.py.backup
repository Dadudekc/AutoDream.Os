"""Central logging configuration for AutoDream.

Provides a single function to configure logging across the
application. Log level can be controlled with environment variables
`LOG_LEVEL` and log output can be sent to a file using `LOG_FILE`.
"""

import os

from src.utils.stability_improvements import stability_manager, safe_import
from utils.logging_setup import LoggingSetup


def configure_logging() -> None:
    """Configure logging for the application."""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE")
    LoggingSetup.setup_logging(log_level, log_file)
