from __future__ import annotations

import argparse
from typing import Optional


def route_command(args: argparse.Namespace) -> Optional[str]:
    """Determine which executor handler should process the command.

    The router inspects parsed arguments and returns the name of the
    corresponding :class:`CommandExecutor` method. Unknown command
    combinations return ``None`` allowing the caller to handle them.
    """
    if getattr(args, "validate", False):
        return "handle_validation"
    if getattr(args, "bulk", False):
        return "handle_bulk_messaging"
    if getattr(args, "campaign", False):
        return "handle_campaign_messaging"
    if getattr(args, "yolo", False):
        return "handle_yolo_messaging"
    if getattr(args, "agent", None):
        return "handle_single_agent_messaging"
    if getattr(args, "message", None):
        # default to bulk messaging when a message is provided without agent
        return "handle_bulk_messaging"
    return None
