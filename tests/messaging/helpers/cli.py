"""Shared helpers for messaging CLI tests."""

from __future__ import annotations

import sys
import types
from typing import List

stub_logger = types.ModuleType("src.utils.logger")


def _get_logger(name: str):
    import logging

    return logging.getLogger(name)


stub_logger.get_logger = _get_logger
sys.modules.setdefault("src.utils.logger", stub_logger)

from src.services.messaging_cli import create_enhanced_parser  # noqa: E402


def parse_flags(args: List[str]):
    """Parse a list of CLI arguments using the enhanced parser."""
    parser = create_enhanced_parser()
    return parser.parse_args(args)
