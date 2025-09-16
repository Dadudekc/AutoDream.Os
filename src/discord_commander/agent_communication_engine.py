#!/usr/bin/env python3
"""
Agent Communication Engine - V2 Compliance Consolidated Module
==============================================================

Consolidated agent communication operations for Discord commander.
Merges base, core, and operations functionality into a single module.

Author: Agent-3 (Infrastructure & DevOps) - V2 Consolidation
License: MIT
"""

import asyncio
import logging
import os
from abc import ABC
from datetime import datetime
from typing import Any

try:
    from ...utils.unified_utilities import get_unified_utility
    from .discord_commander_models import CommandResult, create_command_result
except ImportError:
    # Fallback for direct execution
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from utils.unified_utilities import get_unified_utility
    from discord_commander_models import CommandResult, create_command_result


class AgentCommunicationEngine(ABC):
    """Consolidated agent communication engine for Discord commander"""

    def __init__(self) -> None:
        """Initialize consolidated communication engine."""
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logger for communication engine."""
        logger = logging.getLogger("discord_commander")
        logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _get_unified_utility(self):
        """Get unified utility instance."""
        return get_unified_utility()

    def validate_agent_name(self, agent: str) -> bool:
        """Validate agent name format."""
        if not agent or not isinstance(agent, str):
            return False
        return agent.startswith("Agent-") and len(agent) >= 7

    def format_timestamp(self) -> str:
        """Format current timestamp."""
        return datetime.utcnow().isoformat()

    def create_message_metadata(
        self, sender: str, recipient: str, priority: str = "NORMAL"
    ) -> dict:
        """Create message metadata."""
        return {
            "sender": sender,
            "recipient": recipient,
            "priority": priority,
            "timestamp": self.format_timestamp(),
            "source": "discord_commander",
        }

    async def send_to_agent_inbox(self, agent: str, message: str, sender: str) -> CommandResult:
        """Send message directly to agent's inbox using the messaging system"""
        try:
            # Try to use the consolidated messaging system first
            try:
                from ...services.consolidated_messaging_service import ConsolidatedMessagingService
                
                # Get messaging service instance
                messaging_service = ConsolidatedMessagingService()
                
                # Send via messaging system with simplified interface
                success = messaging_service.send_message(agent, message, sender)
                
                if success:
                    self.logger.info(f"Message sent to {agent} via messaging system")
                    return create_command_result(
                        success=True,
                        message=f"Message successfully delivered to {agent} via messaging system",
                        data={"method": "messaging_system", "agent": agent},
                        agent=agent,
                    )
                else:
                    # Fallback to inbox file method
                    self.logger.warning(f"Messaging system failed for {agent}, falling back to inbox file")
                    
            except ImportError as e:
                self.logger.warning(f"Messaging system not available: {e}, using inbox file method")
            except Exception as e:
                self.logger.warning(f"Messaging system error: {e}, using inbox file method")
            
            # Fallback: Create inbox path
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
                data={"filename": message_filename, "path": message_file_path, "method": "inbox_file"},
                agent=agent,
            )

        except Exception as e:
            self.logger.error(f"Failed to send message to {agent}: {e}")
            return create_command_result(
                success=False,
                message=(f"Failed to deliver message to {agent}: {str(e)}"),
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

    async def broadcast_to_all_agents(self, message: str, sender: str) -> CommandResult:
        """Broadcast message to all agents using the messaging system"""
        try:
            # Try to use the consolidated messaging system first
            try:
                from ...services.consolidated_messaging_service import ConsolidatedMessagingService
                
                # Get messaging service instance
                messaging_service = ConsolidatedMessagingService()
                
                # Use the messaging system for broadcast
                results = messaging_service.broadcast_message(message, sender)
                
                successful_count = sum(1 for success in results.values() if success)
                total_count = len(results)
                
                if successful_count > 0:
                    self.logger.info(f"Broadcast sent to {successful_count}/{total_count} agents via messaging system")
                    return create_command_result(
                        success=True,
                        message=f"Broadcast successfully delivered to {successful_count}/{total_count} agents via messaging system",
                        data={
                            "successful_deliveries": successful_count,
                            "total_agents": total_count,
                            "method": "messaging_system",
                            "results": results
                        },
                    )
                else:
                    self.logger.warning("Messaging system broadcast failed, falling back to individual messages")
                    
            except ImportError as e:
                self.logger.warning(f"Messaging system not available: {e}, using individual messages")
            except Exception as e:
                self.logger.warning(f"Messaging system error: {e}, using individual messages")
            
            # Fallback: Send individual messages
            agents = [f"Agent-{i}" for i in range(1, 9)]
            successful_deliveries = 0
            failed_deliveries = []

            for agent in agents:
                result = await self.send_to_agent_inbox(agent, message, sender)
                if result.success:
                    successful_deliveries += 1
                else:
                    failed_deliveries.append(f"{agent}: {result.message}")

            if successful_deliveries == len(agents):
                return create_command_result(
                    success=True,
                    message=(f"Broadcast successfully delivered to all {len(agents)} agents"),
                    data={
                        "successful_deliveries": successful_deliveries,
                        "total_agents": len(agents),
                        "method": "individual_messages"
                    },
                )
            else:
                return create_command_result(
                    success=False,
                    message=(
                        f"Broadcast partially failed: {successful_deliveries}/"
                        f"{len(agents)} delivered"
                    ),
                    data={
                        "successful_deliveries": successful_deliveries,
                        "failed_deliveries": failed_deliveries,
                        "method": "individual_messages"
                    },
                )

        except Exception as e:
            self.logger.error(f"Failed to broadcast to all agents: {e}")
            return create_command_result(success=False, message=f"Broadcast failed: {str(e)}")

    async def send_human_prompt_to_captain(self, prompt: str, sender: str) -> CommandResult:
        """Send human prompt to Captain Agent-4"""
        try:
            return await self.send_to_agent_inbox("Agent-4", prompt, sender)
        except Exception as e:
            self.logger.error(f"Failed to send human prompt to Captain: {e}")
            return create_command_result(
                success=False,
                message=f"Failed to send human prompt to Captain: {str(e)}",
            )

    def get_agent_status_file_path(self, agent: str) -> str:
        """Get agent status file path"""
        return self._get_unified_utility().path.join(
            os.getcwd(), "agent_workspaces", agent, "status.json"
        )

    async def read_agent_status(self, agent: str) -> dict[str, Any] | None:
        """Read agent status from file"""
        try:
            status_file = self.get_agent_status_file_path(agent)

            if self._get_unified_utility().path.exists(status_file):
                with open(status_file) as f:
                    import json
                    return json.load(f)
            else:
                self.logger.warning(f"Status file not found for {agent}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to read status for {agent}: {e}")
            return None

    async def cleanup_old_messages(self, agent: str, max_age_hours: int = 24) -> int:
        """Clean up old messages from agent's inbox"""
        try:
            inbox_path = self._get_unified_utility().path.join(
                os.getcwd(), "agent_workspaces", agent, "inbox"
            )

            if not self._get_unified_utility().path.exists(inbox_path):
                return 0

            cleaned_count = 0
            current_time = datetime.utcnow().timestamp()
            max_age_seconds = max_age_hours * 3600

            for filename in os.listdir(inbox_path):
                if filename.endswith(".md"):
                    file_path = self._get_unified_utility().path.join(inbox_path, filename)
                    file_age = current_time - os.path.getmtime(file_path)

                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        cleaned_count += 1

            self.logger.info(f"Cleaned up {cleaned_count} old messages from {agent}'s inbox")
            return cleaned_count

        except Exception as e:
            self.logger.error(f"Failed to cleanup old messages for {agent}: {e}")
            return 0


# Factory function for dependency injection
def create_agent_communication_engine() -> AgentCommunicationEngine:
    """Factory function to create agent communication engine"""
    return AgentCommunicationEngine()


# Export for DI
__all__ = ["AgentCommunicationEngine", "create_agent_communication_engine"]
