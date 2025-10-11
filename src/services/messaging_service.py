#!/usr/bin/env python3
"""
Consolidated Messaging Service - Stub for Discord Bot
=====================================================

Lightweight stub to enable Discord bot functionality.
Routes messages through messaging_cli.py via subprocess.

V2 Compliance: Simple adapter pattern
"""

import logging
import subprocess
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ConsolidatedMessagingService:
    """Consolidated messaging service adapter for Discord bot."""

    def __init__(self):
        """Initialize messaging service."""
        self.project_root = Path(__file__).parent.parent.parent
        self.messaging_cli = self.project_root / "src" / "services" / "messaging_cli.py"
        logger.info("ConsolidatedMessagingService initialized")

    def send_message(
        self, agent: str, message: str, priority: str = "regular", use_pyautogui: bool = True
    ) -> dict[str, Any]:
        """
        Send message to agent via messaging_cli.py subprocess.

        Args:
            agent: Target agent ID (e.g., "Agent-1")
            message: Message content
            priority: Message priority ("regular" or "urgent")
            use_pyautogui: Whether to use PyAutoGUI delivery

        Returns:
            Dictionary with success status and message
        """
        try:
            cmd = [
                "python",
                str(self.messaging_cli),
                "--agent",
                agent,
                "--message",
                message,
                "--priority",
                priority,
            ]

            if use_pyautogui:
                cmd.append("--pyautogui")

            # Set PYTHONPATH
            env = {"PYTHONPATH": str(self.project_root)}

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30, env=env, cwd=str(self.project_root)
            )

            if result.returncode == 0:
                logger.info(f"Message sent to {agent}: {message[:50]}...")
                return {"success": True, "message": f"Message sent to {agent}", "agent": agent}
            else:
                error_msg = result.stderr or "Unknown error"
                logger.error(f"Failed to send message to {agent}: {error_msg}")
                return {
                    "success": False,
                    "message": f"Failed to send message: {error_msg}",
                    "agent": agent,
                }

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout sending message to {agent}")
            return {"success": False, "message": "Message timeout", "agent": agent}
        except Exception as e:
            logger.error(f"Error sending message to {agent}: {e}")
            return {"success": False, "message": str(e), "agent": agent}

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        """
        Broadcast message to all agents.

        Args:
            message: Message content
            priority: Message priority

        Returns:
            Dictionary with success status
        """
        agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]

        results = []
        for agent in agents:
            result = self.send_message(agent, message, priority)
            results.append(result)

        success_count = sum(1 for r in results if r.get("success"))

        return {
            "success": success_count > 0,
            "message": f"Broadcast sent to {success_count}/{len(agents)} agents",
            "results": results,
        }

    def get_agent_status(self, agent: str) -> dict[str, Any]:
        """
        Get agent status (stub - returns basic info).

        Args:
            agent: Agent ID

        Returns:
            Dictionary with agent status
        """
        return {"agent": agent, "status": "online", "message": "Status check via Discord"}

    def list_agents(self) -> list[str]:
        """
        List all available agents.

        Returns:
            List of agent IDs
        """
        return [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]
