"""
Discord Bot Commands - V2 Compliant
==================================

Command implementations for Discord Commander bot.
Provides agent control and system interaction commands.

Author: Agent-6 (SSOT_MANAGER)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class DiscordBotCommands:
    """Discord bot command implementations"""
    
    def __init__(self, bot_core):
        """Initialize Discord bot commands"""
        self.bot_core = bot_core
        self.logger = logging.getLogger(__name__)
    
    async def handle_agent_status(self, ctx, agent_id: str = None) -> str:
        """Handle agent status command"""
        try:
            if hasattr(self.bot_core, 'agent_interface'):
                status = self.bot_core.agent_interface.get_agent_status(agent_id)
                return self._format_agent_status(status, agent_id)
            else:
                return "❌ Agent interface not available"
        except Exception as e:
            self.logger.error(f"Error in agent_status command: {e}")
            return f"Error getting agent status: {e}"
    
    async def handle_send_message(self, ctx, agent_id: str, message: str) -> str:
        """Handle send message command"""
        try:
            if hasattr(self.bot_core, 'agent_interface'):
                result = self.bot_core.agent_interface.send_message_to_agent(
                    agent_id, message, from_agent="Discord"
                )
                if result.get("success"):
                    return f"✅ Message sent to {agent_id}"
                else:
                    return f"❌ Failed to send message: {result.get('error')}"
            else:
                return "❌ Agent interface not available"
        except Exception as e:
            self.logger.error(f"Error in send_message command: {e}")
            return f"Error sending message: {e}"
    
    async def handle_swarm_status(self, ctx) -> str:
        """Handle swarm status command"""
        try:
            if hasattr(self.bot_core, 'swarm_coordinator'):
                status = self.bot_core.swarm_coordinator.get_swarm_status()
                return self._format_swarm_status(status)
            else:
                return "❌ Swarm coordinator not available"
        except Exception as e:
            self.logger.error(f"Error in swarm_status command: {e}")
            return f"Error getting swarm status: {e}"
    
    async def handle_activate_agent(self, ctx, agent_id: str) -> str:
        """Handle activate agent command"""
        try:
            if hasattr(self.bot_core, 'agent_interface'):
                result = self.bot_core.agent_interface.activate_agent(agent_id)
                if result.get("success"):
                    return f"✅ {agent_id} activated"
                else:
                    return f"❌ Failed to activate: {result.get('error')}"
            else:
                return "❌ Agent interface not available"
        except Exception as e:
            self.logger.error(f"Error in activate_agent command: {e}")
            return f"Error activating agent: {e}"
    
    async def handle_help(self, ctx) -> str:
        """Handle help command"""
        return """🤖 Discord Commander - Agent Control Hub

**Available Commands:**
- `/agent_status [agent_id]` - Get agent status
- `/send_message <agent_id> <message>` - Send message to agent
- `/swarm_status` - Get swarm coordination status
- `/activate_agent <agent_id>` - Activate an agent
- `/help` - Show this help message

**Examples:**
- `/send_message Agent-5 Check project status`
- `/agent_status Agent-4`
- `/activate_agent Agent-1`
"""
    
    def _format_agent_status(self, status: Any, agent_id: str = None) -> str:
        """Format agent status for Discord"""
        if agent_id:
            if isinstance(status, dict):
                agent_status = status.get("status", "UNKNOWN")
                role = status.get("current_role", "NONE")
                return f"**{agent_id}**: {agent_status} | Role: {role}"
            return f"**{agent_id}**: Error retrieving status"
        else:
            if isinstance(status, dict):
                lines = ["**Agent Status:**"]
                for aid, astat in status.items():
                    if isinstance(astat, dict):
                        lines.append(f"• {aid}: {astat.get('status', 'UNKNOWN')}")
                return "\n".join(lines)
            return "Error retrieving agent statuses"
    
    def _format_swarm_status(self, status: Dict[str, Any]) -> str:
        """Format swarm status for Discord"""
        active = status.get("active_agents", 0)
        total = status.get("total_agents", 0)
        health = status.get("swarm_health", 0)
        
        return f"""**Swarm Status:**
Active Agents: {active}/{total}
Swarm Health: {health:.1f}%
Status: {"✅ GOOD" if health >= 60 else "⚠️ NEEDS ATTENTION"}
"""
