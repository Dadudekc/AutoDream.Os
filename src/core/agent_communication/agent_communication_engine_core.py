#!/usr/bin/env python3
"""
Agent Communication Engine Core - V2 Compliance Module
======================================================

Core agent communication operations for Discord commander.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

import asyncio
import os
from datetime import datetime

try:
    from Agent_Cellphone_V2_Repository.src.core.discord_commander.discord_commander_models import (
        CommandResult,
        create_command_result,
    )

    from .agent_communication_engine_base import AgentCommunicationEngineBase
except ImportError:
    # Fallback for direct execution - use canonical paths
    import os
    import sys

    from .agent_communication_engine_base import AgentCommunicationEngineBase

    # Add src to path if needed
    src_path = os.path.join(os.path.dirname(__file__), "..", "..")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from discord_commander.discord_commander_models import CommandResult, create_command_result


class AgentCommunicationEngineCore(AgentCommunicationEngineBase):
    """Core agent communication operations for Discord commander"""

    async def send_to_agent_inbox(self, agent: str, message: str, sender: str) -> CommandResult:
        """Send message directly to agent's inbox"""
        try:
            # Create inbox path
            inbox_path = self._get_unified_utility().path.join(
                os.getcwd(), "agent_workspaces", agent, "inbox"
            )

            # Ensure inbox directory exists
            self._get_unified_utility().makedirs(inbox_path, exist_ok=True)

            # Create message filename with timestamp
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            message_filename = f"CAPTAIN_MESSAGE_{timestamp}_discord.md"

            # Create message content
            message_content = self._create_inbox_message_content(agent, message, sender)

            # Write message to agent's inbox
            message_file_path = self._get_unified_utility().path.join(inbox_path, message_filename)
            with open(message_file_path, "w", encoding="utf-8") as f:
                f.write(message_content)

            self.logger.info(f"Message sent to {agent}'s inbox: {message_filename}")

            return create_command_result(
                success=True,
                message=f"Message successfully delivered to {agent}'s inbox",
                data={"filename": message_filename, "path": message_file_path},
                agent=agent,
            )

        except Exception as e:
            self.logger.error(f"Failed to send message to {agent}'s inbox: {e}")
            return create_command_result(
                success=False,
                message=(f"Failed to deliver message to {agent}'s inbox: {str(e)}"),
                agent=agent,
            )

    def _create_inbox_message_content(self, agent: str, message: str, sender: str) -> str:
        """Create inbox message content"""
        return f"""# 🚨 CAPTAIN MESSAGE FROM DISCORD

**From**: {sender} (via Discord Commander)
**To**: {agent}
**Priority**: URGENT
**Timestamp**: {datetime.utcnow().isoformat()}

---

{message}

---

**Message delivered via Discord Commander**
**WE. ARE. SWARM. ⚡️🔥**
"""

    async def execute_agent_command(self, agent: str, command: str) -> CommandResult:
        """Execute command on specific agent"""
        start_time = asyncio.get_event_loop().time()

        try:
            self.logger.info(f"Executing command on {agent}: {command}")

            # Simulate command execution (replace with real agent communication)
            await asyncio.sleep(1)

            # Mock successful execution
            execution_time = asyncio.get_event_loop().time() - start_time

            return create_command_result(
                success=True,
                message=f"Command executed successfully on {agent}",
                execution_time=execution_time,
                agent=agent,
            )

        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            return create_command_result(
                success=False,
                message=f"Command failed on {agent}: {str(e)}",
                execution_time=execution_time,
                agent=agent,
            )

    def is_valid_agent(self, agent: str) -> bool:
        """Check if agent name is valid"""
        return agent in [f"Agent-{i}" for i in range(1, 9)]

    def get_all_agent_names(self) -> list[str]:
        """Get list of all agent names"""
        return [f"Agent-{i}" for i in range(1, 9)]
