"""
Agent Status Repository
=======================

Repository for agent status data access using Repository pattern.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Large File Modularization and V2 Compliance
Contract: CONTRACT_Agent-2_1757826687
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class AgentStatusRepository:
    """Repository for agent status data access."""
    
    def __init__(self, base_path: str = "agent_workspaces"):
        """Initialize repository."""
        self.base_path = Path(base_path)
        
    def load_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load agent status from file."""
        try:
            status_file = self.base_path / agent_id / "status.json"
            if status_file.exists():
                with open(status_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"❌ Failed to load status for {agent_id}: {e}")
            return None
            
    def save_agent_status(self, agent_id: str, status_data: Dict[str, Any]) -> bool:
        """Save agent status to file."""
        try:
            status_file = self.base_path / agent_id / "status.json"
            status_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(status_file, 'w') as f:
                json.dump(status_data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to save status for {agent_id}: {e}")
            return False
            
    def get_all_agent_statuses(self, agent_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get status for all agents."""
        statuses = {}
        for agent_id in agent_ids:
            status = self.load_agent_status(agent_id)
            if status:
                statuses[agent_id] = status
        return statuses
        
    def is_agent_onboarded(self, agent_id: str) -> bool:
        """Check if agent is onboarded."""
        status = self.load_agent_status(agent_id)
        if not status:
            return False
            
        # Check multiple onboarding indicators
        return (status.get('onboarding_status') == 'COMPLETED' or 
                status.get('status') == 'onboarded' or
                status.get('status') == 'OPERATIONAL')
                
    def get_agent_fsm_state(self, agent_id: str) -> Optional[str]:
        """Get agent FSM state."""
        status = self.load_agent_status(agent_id)
        if not status:
            return None
            
        fsm_data = status.get('fsm_state', {})
        if isinstance(fsm_data, dict):
            return fsm_data.get('current_state', 'uninitialized')
        else:
            return fsm_data

