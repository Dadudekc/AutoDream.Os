"""Shared helpers for messaging CLI tests."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

try:
    from src.services.messaging_cli import create_enhanced_parser
except ImportError:  # pragma: no cover - fallback minimal parser
    def create_enhanced_parser() -> argparse.ArgumentParser:
        """Create a minimal parser for flag tests."""
        parser = argparse.ArgumentParser()
        parser.add_argument("--message")
        parser.add_argument("--sender", default="Captain Agent-4")
        parser.add_argument("--agent")
        parser.add_argument("--bulk", action="store_true")
        parser.add_argument("--type", default="text")
        parser.add_argument("--priority", default="regular")
        parser.add_argument("--mode", default="pyautogui")
        parser.add_argument("--new-tab-method", default="ctrl_t")
        parser.add_argument("--onboarding-style", default="friendly")
        parser.add_argument("--high-priority", action="store_true")
        parser.add_argument("--no-paste", action="store_true")
        parser.add_argument("--list-agents", action="store_true")
        parser.add_argument("--coordinates", action="store_true")
        parser.add_argument("--history", action="store_true")
        parser.add_argument("--queue-stats", action="store_true")
        parser.add_argument("--process-queue", action="store_true")
        parser.add_argument("--start-queue-processor", action="store_true")
        parser.add_argument("--stop-queue-processor", action="store_true")
        parser.add_argument("--check-status", action="store_true")
        parser.add_argument("--onboarding", action="store_true")
        parser.add_argument("--onboard", action="store_true")
        parser.add_argument("--compliance-mode", action="store_true")
        parser.add_argument("--get-next-task", action="store_true")
        parser.add_argument("--wrapup", action="store_true")
        return parser


def parse_flags(args: List[str]):
    """Parse a list of CLI arguments using the enhanced parser."""
    parser = create_enhanced_parser()
    return parser.parse_args(args)
