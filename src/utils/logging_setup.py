#!/usr/bin/env python3
"""
Logging Setup Module - Logging Configuration

This module provides logging configuration functionality.
Follows Single Responsibility Principle - only logging setup.
Architecture: Single Responsibility Principle - logging setup only
LOC: 80 lines (under 200 limit)
"""

import logging
from typing import Optional, Dict, Any
from pathlib import Path

from src.utils.stability_improvements import stability_manager, safe_import
from src.utils.unified_logging_manager import get_logger


class LoggingSetup:
    """Logging configuration and setup utilities"""

    @staticmethod
    def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> bool:
        """Setup logging configuration using the unified manager"""
        try:
            logger = get_logger("root", log_level)
            if log_file:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(
                    logging.Formatter("%(asctime)s | %(levelname)8s | %(message)s")
                )
                logger.addHandler(file_handler)
            return True
        except Exception as e:
            print(f"Failed to setup logging: {e}")
            return False

    @staticmethod
    def get_logger(name: str, level: str = "INFO") -> logging.Logger:
        """Get a configured logger instance"""
        return get_logger(name, level)

    @staticmethod
    def configure_logging_from_dict(config: Dict[str, Any]) -> bool:
        """Configure logging from a configuration dictionary"""
        try:
            log_level = config.get("log_level", "INFO")
            log_file = config.get("log_file")
            return LoggingSetup.setup_logging(log_level, log_file)
        except Exception as e:
            print(f"Failed to configure logging from dict: {e}")
            return False
