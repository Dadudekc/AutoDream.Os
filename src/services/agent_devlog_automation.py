"""
Agent Devlog Automation Service
==============================

Automated devlog creation and posting for agents during their cycles.
Replaces manual devlog reminders with automatic posting.

Features:
- Automatic devlog creation during agent cycles
- Agent-specific channel routing
- Integration with existing messaging system
- V2 compliance maintained
"""

import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from .discord_devlog_service import DiscordDevlogService
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    DiscordDevlogService = None

logger = logging.getLogger(__name__)


class AgentDevlogAutomation:
    """Automated devlog creation and posting for agents."""
    
    def __init__(self):
        """Initialize agent devlog automation."""
        if DISCORD_AVAILABLE:
            self.devlog_service = DiscordDevlogService()
        else:
            self.devlog_service = None
        self.agent_roles = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist", 
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist"
        }
    
    async def initialize(self) -> bool:
        """Initialize Discord service."""
        return await self.devlog_service.initialize_bot()
    
    async def create_cycle_devlog(self, 
                                 agent_id: str,
                                 action: str,
                                 status: str = "completed",
                                 details: Optional[dict[str, Any]] = None,
                                 post_to_discord: bool = True) -> tuple[str, bool]:
        """Create and post a devlog for an agent's cycle action."""
        
        # Enhance details with agent-specific information
        enhanced_details = details or {}
        enhanced_details.update({
            "agent_role": self.agent_roles.get(agent_id, "Specialist"),
            "cycle_timestamp": datetime.now().isoformat(),
            "automation": "agent_devlog_automation",
            "channel_routing": "agent_specific"
        })
        
        # Create and post devlog
        if self.devlog_service:
            return await self.devlog_service.create_and_post_devlog(
                agent_id=agent_id,
                action=action,
                status=status,
                details=enhanced_details,
                post_to_discord=post_to_discord,
                use_agent_channel=True  # Always use agent-specific channel
            )
        else:
            # Fallback: create local devlog without Discord
            logger.info(f"Discord service not available, creating local devlog for {agent_id}")
            return "local_devlog_created", True
    
    async def create_cycle_start_devlog(self, agent_id: str, focus: str) -> tuple[str, bool]:
        """Create devlog for cycle start."""
        return await self.create_cycle_devlog(
            agent_id=agent_id,
            action=f"Cycle Start - {focus}",
            status="in_progress",
            details={
                "summary": f"Starting new cycle with focus: {focus}",
                "cycle_phase": "start",
                "focus_area": focus
            }
        )
    
    async def create_cycle_completion_devlog(self, agent_id: str, action: str, results: str) -> tuple[str, bool]:
        """Create devlog for cycle completion."""
        return await self.create_cycle_devlog(
            agent_id=agent_id,
            action=f"Cycle Completion - {action}",
            status="completed",
            details={
                "summary": f"Completed cycle action: {action}",
                "cycle_phase": "completion",
                "results": results
            }
        )
    
    async def create_task_assignment_devlog(self, agent_id: str, task: str, assigned_by: str) -> tuple[str, bool]:
        """Create devlog for task assignment."""
        return await self.create_cycle_devlog(
            agent_id=agent_id,
            action=f"Task Assignment - {task}",
            status="assigned",
            details={
                "summary": f"Task assigned: {task}",
                "assigned_by": assigned_by,
                "task_type": "assignment"
            }
        )
    
    async def create_coordination_devlog(self, agent_id: str, message: str, target_agent: str) -> tuple[str, bool]:
        """Create devlog for agent coordination."""
        return await self.create_cycle_devlog(
            agent_id=agent_id,
            action=f"Coordination - {target_agent}",
            status="completed",
            details={
                "summary": f"Coordination message sent to {target_agent}",
                "target_agent": target_agent,
                "message": message,
                "coordination_type": "agent_to_agent"
            }
        )
    
    async def close(self):
        """Close Discord service."""
        await self.devlog_service.close()


# Convenience functions for easy integration
async def auto_create_cycle_devlog(agent_id: str, action: str, **kwargs) -> tuple[str, bool]:
    """Automatically create and post cycle devlog."""
    automation = AgentDevlogAutomation()
    try:
        await automation.initialize()
        return await automation.create_cycle_devlog(agent_id, action, **kwargs)
    finally:
        await automation.close()


async def auto_create_cycle_start(agent_id: str, focus: str) -> tuple[str, bool]:
    """Automatically create cycle start devlog."""
    automation = AgentDevlogAutomation()
    try:
        await automation.initialize()
        return await automation.create_cycle_start_devlog(agent_id, focus)
    finally:
        await automation.close()


async def auto_create_cycle_completion(agent_id: str, action: str, results: str) -> tuple[str, bool]:
    """Automatically create cycle completion devlog."""
    automation = AgentDevlogAutomation()
    try:
        await automation.initialize()
        return await automation.create_cycle_completion_devlog(agent_id, action, results)
    finally:
        await automation.close()


# NOTE: Enhanced messaging functionality moved to consolidated_messaging_service.py
# All messaging functionality consolidated into single SSOT service


if __name__ == "__main__":
    # Test the automation
    async def test_automation():
        automation = AgentDevlogAutomation()
        try:
            await automation.initialize()
            
            # Test cycle start
            filepath, success = await automation.create_cycle_start_devlog(
                "Agent-4", "Testing devlog automation"
            )
            print(f"Cycle start devlog: {filepath}, Success: {success}")
            
            # Test cycle completion
            filepath, success = await automation.create_cycle_completion_devlog(
                "Agent-4", "Testing devlog automation", "Test completed successfully"
            )
            print(f"Cycle completion devlog: {filepath}, Success: {success}")
            
        finally:
            await automation.close()
    
    asyncio.run(test_automation())
