#!/usr/bin/env python3
"""
Consolidated Messaging Service - V2 Compliant Module with Coordinate Validation
==============================================================================

Unified messaging service with pre-delivery coordinate validation & routing safeguards.
Integrates with improved coordinate loader for robust agent communication.

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Chunk 002 (Services)
License: MIT
"""

from __future__ import annotations
import argparse
import logging
from typing import List, Dict, Any

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore

# Fix imports when running as a script
import sys
from pathlib import Path
if __name__ == "__main__":
    # Add the project root to Python path so we can import src modules
    script_dir = Path(__file__).parent.parent.parent  # Go up to project root
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

from src.core.coordinate_loader import CoordinateLoader, ValidationReport

logger = logging.getLogger(__name__)

class ConsolidatedMessagingService:
    """
    MAIN messaging service with pre-delivery coordinate validation & routing safeguards.
    """

    def __init__(self, coord_path: str):
        self.loader = CoordinateLoader(coord_path)
        self.loader.load()

    # ---------- Validation helpers ----------
    def _validate_coordinates_for_delivery(self, agent_id: str) -> ValidationReport:
        report = self.loader.validate_agent(agent_id)
        for issue in report.issues:
            level = logging.WARNING if issue.level == "WARN" else logging.ERROR
            logger.log(level, "%s: %s", agent_id, issue.message)
        return report

    def _validate_all_agents_for_delivery(self) -> ValidationReport:
        report = self.loader.validate_all()
        for issue in report.issues:
            level = logging.WARNING if issue.level == "WARN" else logging.ERROR
            logger.log(level, "%s: %s", issue.agent_id, issue.message)
        return report

    # ---------- Message Formatting ----------
    def _format_a2a_message(self, from_agent: str, to_agent: str, message: str) -> str:
        """Format message as proper A2A message with headers."""
        return f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: {from_agent}
📥 TO: {to_agent}
Priority: NORMAL
Tags: GENERAL
------------------------------------------------------------
{message}
------------------------------------------------------------
"""

    # ---------- Delivery ----------
    def send_message(self, agent_id: str, message: str, from_agent: str = "Agent-2") -> bool:
        report = self._validate_coordinates_for_delivery(agent_id)
        if not report.is_all_ok():
            # Skip if any ERROR for that agent
            has_error = any(i.level == "ERROR" for i in report.issues)
            if has_error:
                logger.error("Delivery skipped for %s due to validation errors.", agent_id)
                return False

        # Format message as proper A2A message
        formatted_message = self._format_a2a_message(from_agent, agent_id, message)
        coords = self.loader.get_coords(agent_id).tuple
        return self._paste_to_coords(coords, formatted_message)

    def broadcast(self, message: str) -> Dict[str, bool]:
        result: Dict[str, bool] = {}
        report = self._validate_all_agents_for_delivery()
        bad_agents = {i.agent_id for i in report.issues if i.level == "ERROR"}
        for aid in self.loader.get_agent_ids():
            if aid in bad_agents:
                logger.error("Broadcast skip -> %s (validation ERROR)", aid)
                result[aid] = False
                continue
            coords = self.loader.get_coords(aid).tuple
            ok = self._paste_to_coords(coords, message)
            result[aid] = ok
        return result

    # ---------- Low-level paste ----------
    def _paste_to_coords(self, coords, message: str) -> bool:
        # NOTE: This is intentionally conservative: validation runs first.
        try:
            if pyautogui is None or pyperclip is None:
                logger.info("[DRY-RUN] Would paste to %s: %s", coords, message)
                return True
            # Real UI actions (guarded):
            pyautogui.click(coords[0], coords[1])
            # Copy message to clipboard and paste for maximum speed
            pyperclip.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press("enter")
            logger.info("[REAL] Fast-pasted to %s", coords)
            return True
        except Exception as e:
            logger.exception("Paste failed at %s: %s", coords, e)
            return False


# ---------- CLI ----------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser("Consolidated Messaging Service (with validation)")
    p.add_argument("--coords", required=True, help="Path to agent coordinate JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    # Validation suite
    v = sub.add_parser("validate", help="Validate coordinates")
    v.add_argument("--report", action="store_true", help="Print detailed validation report")
    v.add_argument("--show", action="store_true", help="Show current coordinates with status")

    # Single send
    s = sub.add_parser("send", help="Send a message to one agent (validated)")
    s.add_argument("--agent", required=True)
    s.add_argument("--message", required=True)
    s.add_argument("--from", dest="from_agent", default="Agent-2", help="Source agent ID (default: Agent-2)")

    # Broadcast
    b = sub.add_parser("broadcast", help="Broadcast to all validated agents")
    b.add_argument("--message", required=True)

    return p


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    svc = ConsolidatedMessagingService(args.coords)

    if args.cmd == "validate":
        report = svc._validate_all_agents_for_delivery()
        if args.show:
            for aid in svc.loader.get_agent_ids():
                ac = svc.loader.get_coords(aid)
                ar = svc._validate_coordinates_for_delivery(aid)
                status = "OK" if ar.is_all_ok() else "ISSUES"
                print(f"{aid:>8}  @ {ac.tuple}  [{status}]")
        if args.report:
            for line in report.to_lines():
                print(line)
        return 0 if report.is_all_ok() else 2

    if args.cmd == "send":
        ok = svc.send_message(args.agent, args.message, args.from_agent)
        print("DELIVERY_OK" if ok else "DELIVERY_FAILED")
        return 0 if ok else 3

    if args.cmd == "broadcast":
        results = svc.broadcast(args.message)
        ok_count = sum(1 for v in results.values() if v)
        total = len(results)
        print(f"BROADCAST: {ok_count}/{total} delivered")
        return 0 if ok_count == total else 4

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
