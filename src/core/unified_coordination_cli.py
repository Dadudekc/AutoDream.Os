#!/usr/bin/env python3
"""Single source of truth CLI for Agent Cellphone V2."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Dict, List

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Mapping of external command names to "module:function"
EXTERNAL_COMMANDS: Dict[str, str] = {
    "ai": "ai_ml.cli:main",
    "services": "services.cli_interface:main",
    "response": "services.response_capture.cli:main",
    "messaging": "services.enhanced_messaging_cli:main",
    "launch": "launchers.launcher_cli:main",
    "devlog": "core.devlog_cli:main",
    "test": "core.testing.testing_cli:main",
}


def _load_and_run(target: str, args: List[str]) -> None:
    """Import and execute the given module target."""
    module_name, func_name = target.split(":")
    module = importlib.import_module(module_name)
    getattr(module, func_name)(args)


def _coord_main(args: List[str]) -> None:
    """Handle coordination-specific commands."""
    from .unified_coordination_system import UnifiedCoordinationSystem

    system = UnifiedCoordinationSystem()
    parser = argparse.ArgumentParser(prog="coord", description="Coordination controls")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("start")
    sub.add_parser("stop")
    sub.add_parser("status")
    ns = parser.parse_args(args)

    if ns.cmd == "start":
        system.start_coordination_system()
        print("✅ coordination started")
    elif ns.cmd == "stop":
        system.stop_coordination_system()
        print("✅ coordination stopped")
    elif ns.cmd == "status":
        print(system.get_system_health())
    else:
        parser.print_help()


def main(argv: List[str] | None = None) -> None:
    """Unified entry point for all project CLIs."""
    parser = argparse.ArgumentParser(description="Unified Coordination CLI")
    parser.add_argument("command", choices=["coord"] + sorted(EXTERNAL_COMMANDS))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    ns = parser.parse_args(argv)

    if ns.command == "coord":
        _coord_main(ns.args)
    else:
        _load_and_run(EXTERNAL_COMMANDS[ns.command], ns.args)


if __name__ == "__main__":
    main()
