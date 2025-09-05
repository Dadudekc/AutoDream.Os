"""Shared helpers for messaging CLI tests."""

from __future__ import annotations

from typing import List

from src.services.messaging_cli import create_enhanced_parser


def parse_flags(args: List[str]):
    """Parse a list of CLI arguments using the enhanced parser."""
    parser = create_enhanced_parser()
    return parser.parse_args(args)
