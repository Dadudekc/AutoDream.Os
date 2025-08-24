#!/usr/bin/env python3
"""
Logging Setup Module - Logging Configuration

This module provides logging configuration functionality.
Follows Single Responsibility Principle - only logging setup.
Architecture: Single Responsibility Principle - logging setup only
LOC: 80 lines (under 200 limit)
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Optional, Dict, Any
from pathlib import Path


class LoggingSetup:
    """Logging configuration and setup utilities"""

    @staticmethod
    def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> bool:
        """Setup logging configuration"""
        try:
            # Configure logging level
            numeric_level = getattr(logging, log_level.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError(f"Invalid log level: {log_level}")

            # Basic logging configuration
            logging.basicConfig(
                level=numeric_level,
                format="%(asctime)s | %(levelname)8s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            # Add file handler if specified
            if log_file:
                # Ensure log directory exists
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)

                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(
                    logging.Formatter("%(asctime)s | %(levelname)8s | %(message)s")
                )
                logging.getLogger().addHandler(file_handler)

            return True

        except Exception as e:
            print(f"Failed to setup logging: {e}")
            return False

    @staticmethod
    def get_logger(name: str, level: str = "INFO") -> logging.Logger:
        """Get a configured logger instance"""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

        # Add console handler if none exists
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s | %(name)s | %(levelname)8s | %(message)s"
                )
            )
            logger.addHandler(console_handler)

        return logger

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


def run_smoke_test():
    """Run basic functionality test for LoggingSetup"""
    print("🧪 Running LoggingSetup Smoke Test...")

    try:
        # Test basic logging setup
        success = LoggingSetup.setup_logging("DEBUG")
        assert success

        # Test logger creation
        logger = LoggingSetup.get_logger("test_logger", "DEBUG")
        assert logger.name == "test_logger"
        assert logger.level == logging.DEBUG

        # Test dict configuration
        config = {"log_level": "WARNING", "log_file": None}
        success = LoggingSetup.configure_logging_from_dict(config)
        assert success

        print("✅ LoggingSetup Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ LoggingSetup Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for LoggingSetup testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Logging Setup CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--setup", help="Setup logging with level")
    parser.add_argument("--file", help="Setup logging with file output")
    parser.add_argument("--get-logger", help="Get logger with name")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    if args.setup:
        success = LoggingSetup.setup_logging(args.setup)
        print(f"Logging setup: {'✅ Success' if success else '❌ Failed'}")
    elif args.file:
        success = LoggingSetup.setup_logging("INFO", args.file)
        print(f"File logging setup: {'✅ Success' if success else '❌ Failed'}")
    elif args.get_logger:
        logger = LoggingSetup.get_logger(args.get_logger)
        print(f"✅ Logger '{args.get_logger}' created with level {logger.level}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
