#!/usr/bin/env python3
"""
Agent Communication Engine Operations - V2 Compliance Module
============================================================

Extended agent communication operations for Discord commander.

Author: Agent-2 (Architecture & Design Specialist) - V2 Refactoring
License: MIT
"""

import logging
import asyncio
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

from .discord_commander_models import create_command_result


class AgentCommunicationEngineOperations:
    """Extended agent communication operations for Discord commander"""
    
    def __init__(self):
        """Initialize agent communication engine operations"""
        self.logger = logging.getLogger(__name__)
        self._unified_utility = None
    
    def _get_unified_utility(self):
        """Get unified utility instance"""
        if self._unified_utility is None:
            from ..core.unified_utility import get_unified_utility
            self._unified_utility = get_unified_utility()
        return self._unified_utility
    
    async def broadcast_to_all_agents(self, message: str, sender: str) -> CommandResult:
        """Broadcast message to all agents"""
        try:
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
                    message=f"Broadcast successfully delivered to all {len(agents)} agents",
                    data={"successful_deliveries": successful_deliveries, "total_agents": len(agents)}
                )
            else:
                return create_command_result(
                    success=False,
                    message=f"Broadcast partially failed: {successful_deliveries}/{len(agents)} delivered",
                    data={"successful_deliveries": successful_deliveries, "failed_deliveries": failed_deliveries}
                )
                
        except Exception as e:
            self.logger.error(f"Failed to broadcast to all agents: {e}")
            return create_command_result(
                success=False,
                message=f"Broadcast failed: {str(e)}"
            )
    
    async def send_human_prompt_to_captain(self, prompt: str, sender: str) -> CommandResult:
        """Send human prompt to Captain Agent-4"""
        try:
            return await self.send_to_agent_inbox("Agent-4", prompt, sender)
        except Exception as e:
            self.logger.error(f"Failed to send human prompt to Captain: {e}")
            return create_command_result(
                success=False,
                message=f"Failed to send human prompt to Captain: {str(e)}"
            )
    
    def get_agent_status_file_path(self, agent: str) -> str:
        """Get agent status file path"""
        return self._get_unified_utility().path.join(
            os.getcwd(), "agent_workspaces", agent, "status.json"
        )
    
    async def read_agent_status(self, agent: str) -> Optional[Dict[str, Any]]:
        """Read agent status from file"""
        try:
            status_file = self.get_agent_status_file_path(agent)
            
            if self._get_unified_utility().path.exists(status_file):
                with open(status_file, 'r') as f:
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
                if filename.endswith('.md'):
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
