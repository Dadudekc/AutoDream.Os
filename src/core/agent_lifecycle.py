"""
AgentLifecycle - Automated status.json management

Agents use this class instead of manual updates.
STATUS.JSON UPDATES ARE AUTOMATIC - IMPOSSIBLE TO FORGET!

Usage:
    from src.core.agent_lifecycle import AgentLifecycle
    
    lifecycle = AgentLifecycle('Agent-7')
    lifecycle.start_cycle()  # Auto-updates status.json
    lifecycle.start_mission("Mission name", "HIGH")  # Auto-updates
    lifecycle.complete_task("Task done", points=100)  # Auto-updates
    lifecycle.end_cycle(commit=True)  # Auto-commits to git
"""

from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import subprocess


class AgentLifecycle:
    """
    Manages agent lifecycle with automatic status.json updates.
    
    All agent actions (cycle start, mission start, task complete, etc.)
    automatically update status.json - NO manual updates needed!
    """
    
    def __init__(self, agent_id: str):
        """
        Initialize AgentLifecycle for an agent.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
        """
        self.agent_id = agent_id
        self.workspace = Path(f"agent_workspaces/{agent_id}")
        self.status_file = self.workspace / "status.json"
        
        # Ensure workspace exists
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # Load or create status
        self._load_status()
    
    def _load_status(self) -> None:
        """Load current status.json or create default."""
        if self.status_file.exists():
            with open(self.status_file) as f:
                self.status = json.load(f)
        else:
            self.status = self._create_default_status()
            self._save_status()
    
    def _create_default_status(self) -> Dict[str, Any]:
        """Create default status.json structure."""
        return {
            "agent_id": self.agent_id,
            "agent_name": "Agent",
            "status": "IDLE",
            "current_phase": "Initialized",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "current_mission": "No mission assigned",
            "mission_priority": "NONE",
            "cycle_count": 0,
            "fsm_state": "start",
            "current_tasks": [],
            "completed_tasks": [],
            "achievements": [],
            "points_earned": 0,
            "next_actions": ["Await mission assignment"],
            "blockers": []
        }
    
    def _save_status(self) -> None:
        """Save status.json with auto-updated timestamp."""
        self.status['last_updated'] = datetime.now(timezone.utc).isoformat()
        
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2)
    
    def _commit_to_git(self, message: Optional[str] = None) -> bool:
        """
        Commit status.json to git.
        
        Args:
            message: Optional custom commit message
            
        Returns:
            True if commit successful, False otherwise
        """
        try:
            cycle = self.status.get('cycle_count', 0)
            commit_msg = message or f"status: {self.agent_id} cycle {cycle} complete"
            
            subprocess.run(['git', 'add', str(self.status_file)], check=True)
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    # ==================== LIFECYCLE METHODS ====================
    
    def start_cycle(self) -> None:
        """
        AUTOMATIC status update on cycle start.
        
        Updates:
            - status: "ACTIVE"
            - fsm_state: "active"
            - cycle_count: +1
            - last_cycle: current timestamp
        """
        self.status.update({
            'status': 'ACTIVE',
            'fsm_state': 'active',
            'cycle_count': self.status.get('cycle_count', 0) + 1,
            'last_cycle': datetime.now(timezone.utc).isoformat()
        })
        self._save_status()
        
        cycle_num = self.status['cycle_count']
        print(f"✅ {self.agent_id}: Cycle {cycle_num} started")
    
    def start_mission(self, mission_name: str, priority: str = "MEDIUM") -> None:
        """
        AUTOMATIC status update when mission starts.
        
        Args:
            mission_name: Mission description
            priority: Mission priority (CRITICAL, HIGH, MEDIUM, LOW)
        """
        self.status.update({
            'current_mission': mission_name,
            'mission_priority': priority.upper(),
            'current_phase': 'Mission started',
            'status': 'ACTIVE',
            'fsm_state': 'active',
            'current_tasks': [],
            'blockers': []
        })
        self._save_status()
        
        print(f"✅ {self.agent_id}: Mission started - {mission_name} (Priority: {priority})")
    
    def update_phase(self, phase_description: str) -> None:
        """
        AUTOMATIC status update for phase changes.
        
        Args:
            phase_description: Current work phase description
        """
        self.status['current_phase'] = phase_description
        self._save_status()
        
        print(f"🔄 {self.agent_id}: Phase - {phase_description}")
    
    def add_task(self, task_name: str) -> None:
        """
        Add task to current_tasks list.
        
        Args:
            task_name: Task description
        """
        if 'current_tasks' not in self.status:
            self.status['current_tasks'] = []
        
        self.status['current_tasks'].append(task_name)
        self._save_status()
        
        print(f"📋 {self.agent_id}: Task added - {task_name}")
    
    def complete_task(self, task_name: str, points: int = 0) -> None:
        """
        AUTOMATIC status update when task completes.
        
        Args:
            task_name: Task description
            points: Points earned for task completion
        """
        # Add to completed_tasks
        if 'completed_tasks' not in self.status:
            self.status['completed_tasks'] = []
        self.status['completed_tasks'].append(task_name)
        
        # Remove from current_tasks if exists
        if task_name in self.status.get('current_tasks', []):
            self.status['current_tasks'].remove(task_name)
        
        # Add points
        self.status['points_earned'] = self.status.get('points_earned', 0) + points
        
        self._save_status()
        
        total_points = self.status['points_earned']
        print(f"✅ {self.agent_id}: Task complete - {task_name} (+{points} pts, total: {total_points})")
    
    def add_blocker(self, blocker_description: str) -> None:
        """
        Add blocker and set status to BLOCKED.
        
        Args:
            blocker_description: Description of what's blocking progress
        """
        if 'blockers' not in self.status:
            self.status['blockers'] = []
        
        self.status['blockers'].append(blocker_description)
        self.status['status'] = 'BLOCKED'
        self.status['fsm_state'] = 'blocked'
        self._save_status()
        
        print(f"⚠️ {self.agent_id}: BLOCKED - {blocker_description}")
    
    def clear_blockers(self) -> None:
        """Clear all blockers and resume ACTIVE status."""
        self.status['blockers'] = []
        self.status['status'] = 'ACTIVE'
        self.status['fsm_state'] = 'active'
        self._save_status()
        
        print(f"✅ {self.agent_id}: Blockers cleared - resuming ACTIVE")
    
    def add_achievement(self, achievement: str) -> None:
        """
        Add achievement to agent's record.
        
        Args:
            achievement: Achievement description
        """
        if 'achievements' not in self.status:
            self.status['achievements'] = []
        
        self.status['achievements'].append(achievement)
        self._save_status()
        
        print(f"🏆 {self.agent_id}: Achievement - {achievement}")
    
    def set_next_actions(self, actions: List[str]) -> None:
        """
        Set planned next actions.
        
        Args:
            actions: List of next action descriptions
        """
        self.status['next_actions'] = actions
        self._save_status()
        
        print(f"📋 {self.agent_id}: Next actions set ({len(actions)} items)")
    
    def complete_mission(self) -> None:
        """Mark current mission as complete."""
        self.status.update({
            'status': 'COMPLETE',
            'fsm_state': 'complete',
            'current_phase': f"{self.status['current_mission']} - COMPLETE",
            'current_tasks': [],
            'next_actions': ['Await next mission assignment']
        })
        self._save_status()
        
        mission = self.status['current_mission']
        points = self.status.get('points_earned', 0)
        print(f"🎯 {self.agent_id}: Mission COMPLETE - {mission} ({points} total points)")
    
    def end_cycle(self, commit: bool = False) -> None:
        """
        AUTOMATIC status update on cycle end.
        
        Args:
            commit: If True, also commit status.json to git
        """
        self.status['last_updated'] = datetime.now(timezone.utc).isoformat()
        self._save_status()
        
        cycle_num = self.status['cycle_count']
        
        if commit:
            if self._commit_to_git():
                print(f"✅ {self.agent_id}: Cycle {cycle_num} ended (committed to git)")
            else:
                print(f"⚠️ {self.agent_id}: Cycle {cycle_num} ended (git commit failed)")
        else:
            print(f"✅ {self.agent_id}: Cycle {cycle_num} ended")
    
    # ==================== UTILITY METHODS ====================
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status dictionary."""
        return self.status.copy()
    
    def get_cycle_count(self) -> int:
        """Get current cycle count."""
        return self.status.get('cycle_count', 0)
    
    def get_points(self) -> int:
        """Get total points earned."""
        return self.status.get('points_earned', 0)
    
    def is_blocked(self) -> bool:
        """Check if agent is currently blocked."""
        return self.status.get('status') == 'BLOCKED'
    
    def get_blockers(self) -> List[str]:
        """Get list of current blockers."""
        return self.status.get('blockers', [])


# ==================== CONVENIENCE FUNCTIONS ====================

def quick_cycle_start(agent_id: str) -> AgentLifecycle:
    """
    Quick helper to start a cycle.
    
    Args:
        agent_id: Agent identifier
        
    Returns:
        AgentLifecycle instance for continued use
    """
    lifecycle = AgentLifecycle(agent_id)
    lifecycle.start_cycle()
    return lifecycle


def quick_task_complete(agent_id: str, task_name: str, points: int = 0) -> None:
    """
    Quick helper to mark task complete.
    
    Args:
        agent_id: Agent identifier
        task_name: Task description
        points: Points earned
    """
    lifecycle = AgentLifecycle(agent_id)
    lifecycle.complete_task(task_name, points)


def quick_cycle_end(agent_id: str, commit: bool = True) -> None:
    """
    Quick helper to end cycle.
    
    Args:
        agent_id: Agent identifier
        commit: Whether to commit to git
    """
    lifecycle = AgentLifecycle(agent_id)
    lifecycle.end_cycle(commit=commit)

