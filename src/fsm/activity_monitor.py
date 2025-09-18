#!/usr/bin/env python3
"""
FSM Activity Monitor - V2 Compliant
===================================

Agent activity monitoring system for FSM state management.
Tracks agent activity and automatically updates states based on inactivity.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .fsm_registry import AgentState, update_agent_state, read_agent_state

# V2 Compliance: File under 400 lines, functions under 30 lines
ACTIVITY_TIMEOUT_MINUTES = 30  # 30 minutes of inactivity = INACTIVE
MESSAGING_TIMEOUT_MINUTES = 15  # 15 minutes without messaging = INACTIVE


class ActivityMonitor:
    """Monitor agent activity and update FSM states accordingly."""
    
    def __init__(self):
        """Initialize activity monitor."""
        self.activity_file = Path("swarm_coordination/agent_activity.json")
        self.activity_data = self._load_activity_data()
    
    def _load_activity_data(self) -> Dict[str, Dict]:
        """Load agent activity data from file."""
        if self.activity_file.exists():
            try:
                return json.loads(self.activity_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {}
    
    def _save_activity_data(self):
        """Save agent activity data to file."""
        try:
            self.activity_file.parent.mkdir(parents=True, exist_ok=True)
            self.activity_file.write_text(
                json.dumps(self.activity_data, indent=2), 
                encoding="utf-8"
            )
        except Exception as e:
            print(f"⚠️  Error saving activity data: {e}")
    
    def record_agent_activity(self, agent_id: str, activity_type: str = "general"):
        """Record agent activity timestamp."""
        current_time = datetime.now().isoformat()
        
        if agent_id not in self.activity_data:
            self.activity_data[agent_id] = {}
        
        self.activity_data[agent_id].update({
            "last_activity": current_time,
            "last_activity_type": activity_type,
            "activity_count": self.activity_data[agent_id].get("activity_count", 0) + 1
        })
        
        self._save_activity_data()
    
    def record_messaging_activity(self, agent_id: str):
        """Record agent messaging activity."""
        self.record_agent_activity(agent_id, "messaging")
    
    def record_task_activity(self, agent_id: str):
        """Record agent task activity."""
        self.record_agent_activity(agent_id, "task")
    
    def record_status_update(self, agent_id: str):
        """Record agent status update activity."""
        self.record_agent_activity(agent_id, "status")
    
    def check_agent_inactivity(self, agent_id: str) -> Tuple[bool, str]:
        """Check if agent is inactive and return status."""
        if agent_id not in self.activity_data:
            return True, "no_activity_recorded"
        
        last_activity_str = self.activity_data[agent_id].get("last_activity")
        if not last_activity_str:
            return True, "no_activity_timestamp"
        
        try:
            last_activity = datetime.fromisoformat(last_activity_str)
            time_since_activity = datetime.now() - last_activity
            
            if time_since_activity > timedelta(minutes=ACTIVITY_TIMEOUT_MINUTES):
                return True, f"inactive_{time_since_activity.total_seconds() / 60:.1f}_minutes"
            
            return False, "active"
        except Exception:
            return True, "invalid_timestamp"
    
    def check_messaging_inactivity(self, agent_id: str) -> Tuple[bool, str]:
        """Check if agent has been inactive in messaging."""
        if agent_id not in self.activity_data:
            return True, "no_messaging_recorded"
        
        last_activity_str = self.activity_data[agent_id].get("last_activity")
        if not last_activity_str:
            return True, "no_messaging_timestamp"
        
        try:
            last_activity = datetime.fromisoformat(last_activity_str)
            time_since_activity = datetime.now() - last_activity
            
            if time_since_activity > timedelta(minutes=MESSAGING_TIMEOUT_MINUTES):
                return True, f"messaging_inactive_{time_since_activity.total_seconds() / 60:.1f}_minutes"
            
            return False, "messaging_active"
        except Exception:
            return True, "invalid_messaging_timestamp"
    
    def update_agent_state_for_inactivity(self, agent_id: str) -> bool:
        """Update agent state to INACTIVE if inactive."""
        is_inactive, reason = self.check_agent_inactivity(agent_id)
        
        if is_inactive:
            current_state = read_agent_state(agent_id)
            if current_state != AgentState.PAUSED.value:
                success = update_agent_state(agent_id, AgentState.PAUSED.value)
                if success:
                    print(f"🔄 Updated {agent_id} to PAUSED due to inactivity: {reason}")
                return success
        return False
    
    def get_agent_activity_summary(self) -> Dict[str, Dict]:
        """Get comprehensive activity summary for all agents."""
        summary = {}
        
        # Get all agent IDs from workspace
        workspace_path = Path("agent_workspaces")
        if workspace_path.exists():
            for agent_dir in workspace_path.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agent_id = agent_dir.name
                    
                    is_inactive, inactivity_reason = self.check_agent_inactivity(agent_id)
                    is_messaging_inactive, messaging_reason = self.check_messaging_inactivity(agent_id)
                    current_state = read_agent_state(agent_id)
                    
                    summary[agent_id] = {
                        "current_state": current_state,
                        "is_inactive": is_inactive,
                        "inactivity_reason": inactivity_reason,
                        "is_messaging_inactive": is_messaging_inactive,
                        "messaging_reason": messaging_reason,
                        "last_activity": self.activity_data.get(agent_id, {}).get("last_activity"),
                        "activity_count": self.activity_data.get(agent_id, {}).get("activity_count", 0)
                    }
        
        return summary
    
    def get_inactive_agents(self) -> List[str]:
        """Get list of inactive agents."""
        inactive_agents = []
        summary = self.get_agent_activity_summary()
        
        for agent_id, data in summary.items():
            if data["is_inactive"]:
                inactive_agents.append(agent_id)
        
        return inactive_agents
    
    def get_messaging_inactive_agents(self) -> List[str]:
        """Get list of agents inactive in messaging."""
        messaging_inactive_agents = []
        summary = self.get_agent_activity_summary()
        
        for agent_id, data in summary.items():
            if data["is_messaging_inactive"]:
                messaging_inactive_agents.append(agent_id)
        
        return messaging_inactive_agents


def get_activity_monitor() -> ActivityMonitor:
    """Get singleton activity monitor instance."""
    if not hasattr(get_activity_monitor, '_instance'):
        get_activity_monitor._instance = ActivityMonitor()
    return get_activity_monitor._instance
