#!/usr/bin/env python3
"""
Workflow Automation - Message Forwarding
=========================================

Handles message forwarding automation for agent workflows.
V2 Compliant: ≤400 lines, focused message forwarding.

Author: Agent-1 (Infrastructure Specialist)
License: MIT
"""

import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class MessageForwardingAutomation:
    """Handles message forwarding automation."""

    def __init__(self, workflow_log_path: Path):
        """Initialize message forwarding automation."""
        self.workflow_log_path = workflow_log_path

    def forward_message(
        self,
        from_agent: str,
        to_agent: str,
        message: str,
        priority: str = "normal",
        project: str = None,
    ) -> bool:
        """Forward message between agents."""
        try:
            # Create message file
            target_dir = Path(f"agent_workspaces/{to_agent}")
            target_dir.mkdir(parents=True, exist_ok=True)

            inbox_dir = target_dir / "inbox"
            inbox_dir.mkdir(exist_ok=True)

            message_data = {
                "from": from_agent,
                "to": to_agent,
                "message": message,
                "priority": priority,
                "project": project,
                "timestamp": datetime.now().isoformat(),
            }

            message_file = inbox_dir / f"message_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(message_file, "w") as f:
                json.dump(message_data, f, indent=2)

            # Try to use messaging system if available
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "messaging_system.py",
                        from_agent,
                        to_agent,
                        message,
                        priority.upper(),
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    logger.info(f"Message forwarded via messaging system: {from_agent} -> {to_agent}")
                else:
                    logger.warning(f"Messaging system failed: {result.stderr}")

            except Exception as e:
                logger.warning(f"Messaging system not available: {e}")

            # Log workflow
            self._log_workflow(
                "message_forwarding",
                {
                    "from": from_agent,
                    "to": to_agent,
                    "priority": priority,
                    "project": project,
                    "status": "success",
                },
            )

            logger.info(f"Message forwarded: {from_agent} -> {to_agent}")
            return True

        except Exception as e:
            logger.error(f"Message forwarding failed: {e}")
            return False

    def broadcast_message(
        self,
        from_agent: str,
        message: str,
        target_agents: list[str],
        priority: str = "normal",
        project: str = None,
    ) -> Dict[str, bool]:
        """Broadcast message to multiple agents."""
        try:
            results = {}
            
            for target_agent in target_agents:
                success = self.forward_message(
                    from_agent=from_agent,
                    to_agent=target_agent,
                    message=message,
                    priority=priority,
                    project=project,
                )
                results[target_agent] = success

            # Log workflow
            self._log_workflow(
                "message_broadcast",
                {
                    "from": from_agent,
                    "targets": target_agents,
                    "priority": priority,
                    "project": project,
                    "results": results,
                    "status": "success",
                },
            )

            logger.info(f"Message broadcasted to {len(target_agents)} agents")
            return results

        except Exception as e:
            logger.error(f"Message broadcast failed: {e}")
            return {}

    def get_agent_messages(self, agent_id: str) -> list:
        """Get messages for an agent."""
        try:
            inbox_dir = Path(f"agent_workspaces/{agent_id}/inbox")
            
            if not inbox_dir.exists():
                return []

            messages = []
            for message_file in inbox_dir.glob("message_*.json"):
                try:
                    with open(message_file, "r") as f:
                        message_data = json.load(f)
                        messages.append(message_data)
                except Exception as e:
                    logger.error(f"Failed to load message file {message_file}: {e}")

            # Sort by timestamp
            messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            return messages

        except Exception as e:
            logger.error(f"Failed to get agent messages: {e}")
            return []

    def clear_agent_messages(self, agent_id: str) -> bool:
        """Clear messages for an agent."""
        try:
            inbox_dir = Path(f"agent_workspaces/{agent_id}/inbox")
            
            if not inbox_dir.exists():
                return True

            # Remove message files
            for message_file in inbox_dir.glob("message_*.json"):
                try:
                    message_file.unlink()
                except Exception as e:
                    logger.error(f"Failed to remove message file {message_file}: {e}")

            logger.info(f"Messages cleared for agent {agent_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to clear agent messages: {e}")
            return False

    def _log_workflow(self, action: str, details: Dict[str, Any]) -> None:
        """Log workflow action."""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "details": details,
            }

            # Load existing log
            if self.workflow_log_path.exists():
                with open(self.workflow_log_path, "r") as f:
                    log_data = json.load(f)
            else:
                log_data = {"workflows": []}

            # Add new entry
            log_data["workflows"].append(log_entry)

            # Save updated log
            with open(self.workflow_log_path, "w") as f:
                json.dump(log_data, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to log workflow: {e}")


def create_message_forwarding_automation(workflow_log_path: Path) -> MessageForwardingAutomation:
    """Create message forwarding automation."""
    return MessageForwardingAutomation(workflow_log_path)

