#!/usr/bin/env python3
"""
Gas Messaging - Extracted from Swarm Orchestrator
=================================================

Handles PyAutoGUI message delivery to agents for gas delivery notifications.

Author: Agent-8 (SSOT & System Integration) - Lean Excellence Refactor
License: MIT
"""

import subprocess
import sys
from pathlib import Path
from typing import Any


def send_gas_message(
    agent: str, opportunity: dict[str, Any], roi: float, project_root: Path
) -> bool:
    """
    Send PyAutoGUI message to agent (GAS DELIVERY!).

    Args:
        agent: Target agent ID (e.g., "Agent-1")
        opportunity: Opportunity details dict
        roi: Calculated ROI value
        project_root: Project root path

    Returns:
        True if message sent successfully, False otherwise
    """
    try:
        message = (
            f"⛽ GAS DELIVERY! Auto-task assigned: {opportunity.get('type', 'work')} "
            f"({opportunity.get('points', 100)}pts, ROI {roi:.2f}). "
            f"Check INBOX + Execute NOW! 🔥🐝"
        )

        # Send PyAutoGUI message
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "src.services.messaging_cli",
                "--agent",
                agent,
                "--message",
                message,
                "--priority",
                "regular",
                "--pyautogui",
            ],
            capture_output=True,
            text=True,
            cwd=project_root,
        )

        if result.returncode == 0:
            print(f"  ⛽ Gas delivered to {agent}!")
            return True
        else:
            print(f"  ⚠️  Gas delivery failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"  ❌ Gas delivery error: {e}")
        return False


__all__ = ["send_gas_message"]
