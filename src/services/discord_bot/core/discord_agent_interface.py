"""
Discord Agent Interface - V2 Compliant
=====================================

Interface for Discord-based agent control and coordination.
Provides agent messaging, status checking, and control capabilities.

Author: Agent-6 (SSOT_MANAGER)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class DiscordAgentInterface:
    """Interface for controlling agents via Discord"""
    
    def __init__(self, bot):
        """Initialize Discord agent interface"""
        self.bot = bot
        self.workspace_dir = Path("agent_workspaces")
        self.agents = [f"Agent-{i}" for i in range(1, 9)]
    
    def get_agent_status(self, agent_id: str = None) -> Dict[str, Any]:
        """Get status of one or all agents"""
        if agent_id:
            return self._get_single_agent_status(agent_id)
        else:
            return self._get_all_agent_statuses()
    
    def _get_single_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of a single agent"""
        status_file = self.workspace_dir / agent_id / "status.json"
        
        if not status_file.exists():
            return {
                "agent_id": agent_id,
                "status": "NOT_FOUND",
                "error": "Status file not found"
            }
        
        try:
            with open(status_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading status for {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "status": "ERROR",
                "error": str(e)
            }
    
    def _get_all_agent_statuses(self) -> Dict[str, Any]:
        """Get status of all agents"""
        statuses = {}
        for agent_id in self.agents:
            statuses[agent_id] = self._get_single_agent_status(agent_id)
        return statuses
    
    def send_message_to_agent(self, agent_id: str, message: str, from_agent: str = "Discord") -> Dict[str, Any]:
        """Send message to an agent"""
        try:
            # Create message in agent inbox
            inbox_dir = self.workspace_dir / agent_id / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)
            
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message_file = inbox_dir / f"discord_{timestamp}.txt"
            
            full_message = f"""============================================================
[A2A] MESSAGE - FROM DISCORD
============================================================
📤 FROM: {from_agent} (via Discord)
📥 TO: {agent_id}
Priority: NORMAL
Tags: DISCORD_COMMAND
-------------------------------------------------------------

{message}

-------------------------------------------------------------
Sent via Discord Commander
============================================================
"""
            
            with open(message_file, 'w') as f:
                f.write(full_message)
            
            logger.info(f"Message sent to {agent_id}")
            return {
                "success": True,
                "agent_id": agent_id,
                "message_file": str(message_file)
            }
            
        except Exception as e:
            logger.error(f"Error sending message to {agent_id}: {e}")
            return {
                "success": False,
                "agent_id": agent_id,
                "error": str(e)
            }
    
    def activate_agent(self, agent_id: str) -> Dict[str, Any]:
        """Activate an agent"""
        try:
            status_file = self.workspace_dir / agent_id / "status.json"
            status_file.parent.mkdir(parents=True, exist_ok=True)
            
            if status_file.exists():
                with open(status_file, 'r') as f:
                    status = json.load(f)
            else:
                status = {"agent_id": agent_id}
            
            status["status"] = "ACTIVE"
            status["last_active"] = datetime.now().isoformat()
            
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
            
            logger.info(f"Activated {agent_id}")
            return {"success": True, "agent_id": agent_id, "status": "ACTIVE"}
            
        except Exception as e:
            logger.error(f"Error activating {agent_id}: {e}")
            return {"success": False, "agent_id": agent_id, "error": str(e)}


class DiscordSwarmCoordinator:
    """Coordinator for swarm operations via Discord"""
    
    def __init__(self, bot):
        """Initialize Discord swarm coordinator"""
        self.bot = bot
        self.agent_interface = DiscordAgentInterface(bot)
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Get overall swarm status"""
        agent_statuses = self.agent_interface.get_agent_status()
        
        active_count = sum(
            1 for status in agent_statuses.values() 
            if isinstance(status, dict) and status.get("status") == "ACTIVE"
        )
        
        return {
            "total_agents": len(agent_statuses),
            "active_agents": active_count,
            "agent_statuses": agent_statuses,
            "swarm_health": (active_count / len(agent_statuses)) * 100 if agent_statuses else 0
        }
    
    def broadcast_message(self, message: str, from_agent: str = "Discord") -> Dict[str, Any]:
        """Broadcast message to all agents"""
        results = {}
        for agent_id in self.agent_interface.agents:
            result = self.agent_interface.send_message_to_agent(agent_id, message, from_agent)
            results[agent_id] = result
        return results

