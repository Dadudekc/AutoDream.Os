#!/usr/bin/env python3
"""
Consolidated Messaging Service - PyAutoGUI Agent Communication
=============================================================

Real-time agent-to-agent communication via PyAutoGUI automation.
Fixed and optimized by Agent-2 for swarm coordination.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.coordinate_loader import CoordinateLoader

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService:
    """Consolidated messaging service with PyAutoGUI automation."""

    def __init__(self, coord_path: str = "config/coordinates.json") -> None:
        """Initialize messaging service with coordinate validation."""
        self.loader = CoordinateLoader(coord_path)
        self.loader.load()
        self.validation_report = self.loader.validate_all()

        if not self.validation_report.is_all_ok():
            logger.error("Coordinate validation failed: %s", self.validation_report.issues)
            raise ValueError(f"Invalid coordinates: {self.validation_report.issues}")

        logger.info(
            "Messaging service initialized with %d agents", len(self.loader.get_agent_ids())
        )

    def send_message(
        self, agent_id: str, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL"
    ) -> bool:
        """Send message to specific agent via PyAutoGUI with priority support."""
        try:
            # Validate agent exists
            if agent_id not in self.loader.get_agent_ids():
                logger.error("Unknown agent: %s", agent_id)
                return False

            # Format message with A2A headers and priority
            formatted_message = self._format_a2a_message(from_agent, agent_id, message, priority)

            # Get coordinates and send
            coords = self.loader.get_coords(agent_id).tuple
            return self._paste_to_coords(coords, formatted_message)

        except Exception as e:
            logger.exception("Send message failed: %s", e)
            return False

    def broadcast_message(
        self, message: str, from_agent: str = "Agent-2", priority: str = "NORMAL"
    ) -> dict[str, bool]:
        """Broadcast message to all agents with priority support."""
        results = {}

        for agent_id in self.loader.get_agent_ids():
            try:
                success = self.send_message(agent_id, message, from_agent, priority)
                results[agent_id] = success
            except Exception as e:
                logger.error("Broadcast to %s failed: %s", agent_id, e)
                results[agent_id] = False

        return results

    def _format_a2a_message(
        self, from_agent: str, to_agent: str, message: str, priority: str = "NORMAL"
    ) -> str:
        """Format message as proper A2A message with headers and priority support."""
        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: {priority}
Tags: GENERAL
------------------------------------------------------------
{message}
------------------------------------------------------------
"""

    def _paste_to_coords(self, coords, message: str) -> bool:
        """Paste message to coordinates using PyAutoGUI + pyperclip."""
        try:
            if pyautogui is None or pyperclip is None:
                logger.info("[DRY-RUN] Would paste to %s: %s", coords, message)
                return True

            # Real UI actions (guarded):
            pyautogui.click(coords[0], coords[1])
            # Copy message to clipboard and paste for maximum speed
            pyperclip.copy(message)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            logger.info("[REAL] Fast-pasted to %s", coords)
            return True

        except Exception as e:
            logger.exception("Paste failed at %s: %s", coords, e)
            return False

    def get_status(self) -> dict[str, any]:
        """Get service status."""
        return {
            "validation_report": {
                "ok": self.validation_report.ok,
                "issues": [
                    {"agent_id": i.agent_id, "level": i.level, "message": i.message}
                    for i in self.validation_report.issues
                ],
            },
            "agent_count": len(self.loader.get_agent_ids()),
            "agents": self.loader.get_agent_ids(),
            "pyautogui_available": pyautogui is not None,
            "pyperclip_available": pyperclip is not None,
        }


def build_parser() -> argparse.ArgumentParser:
    """Build command line parser."""
    p = argparse.ArgumentParser(description="Consolidated Messaging Service")
    p.add_argument("--coords", default="config/coordinates.json", help="Coordinate file path")

    sub = p.add_subparsers(dest="cmd", help="Commands")

    # Send command
    s = sub.add_parser("send", help="Send a message to one agent (validated)")
    s.add_argument("--agent", required=True)
    s.add_argument("--message", required=True)
    s.add_argument(
        "--from", dest="from_agent", default="Agent-2", help="Source agent ID (default: Agent-2)"
    )

    # Broadcast command
    b = sub.add_parser("broadcast", help="Broadcast message to all agents")
    b.add_argument("--message", required=True)
    b.add_argument(
        "--from", dest="from_agent", default="Agent-2", help="Source agent ID (default: Agent-2)"
    )

    # Status command
    sub.add_parser("status", help="Show service status")

    return p


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.cmd:
        parser.print_help()
        return 1

    try:
        svc = ConsolidatedMessagingService(args.coords)

        if args.cmd == "send":
            ok = svc.send_message(args.agent, args.message, args.from_agent)
            logger.info("DELIVERY_OK" if ok else "DELIVERY_FAILED")
            return 0 if ok else 3

        elif args.cmd == "broadcast":
            results = svc.broadcast_message(args.message, args.from_agent)
            success_count = sum(1 for success in results.values() if success)
            logger.info(f"BROADCAST_COMPLETE: {success_count}/{len(results)} successful")
            return 0 if success_count == len(results) else 3

        elif args.cmd == "status":
            status = svc.get_status()
            logger.info(f"Service Status: {status}")
            return 0

        else:
            parser.print_help()
            return 1

    except Exception as e:
        logger.error("Service error: %s", e)
        return 2


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
