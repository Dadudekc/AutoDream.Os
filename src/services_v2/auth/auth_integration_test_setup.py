#!/usr/bin/env python3
"""Setup utilities for authentication integration tests."""

import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).resolve().parents[3]))


def setup_logging() -> logging.Logger:
    """Setup comprehensive logging for integration testing."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("auth_integration_tests.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)
