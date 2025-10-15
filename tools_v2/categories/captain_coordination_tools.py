"""
Captain Coordination Tools - V2 Compliant Category
=================================================

Consolidates scattered captain_* coordination tools into single category.

Migrated from tools/ directory as part of Infrastructure Consolidation Mission.
Lead: Agent-2 (Architecture), Execution: Agent-6 (Co-Captain)

Date: 2025-10-15
Status: NEW CATEGORY - Infrastructure Consolidation
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import json
from pathlib import Path
from datetime import datetime


@dataclass
class CaptainTool:
    """Base for captain coordination tools."""
    name: str
    description: str
    category: str = "captain.coordination"


class CompletionProcessor:
    """
    Process agent task completions and update tracking systems.
    
    Migrated from: tools/captain_completion_processor.py
    """
    
    def process_completion(
        self,
        agent_id: str,
        task_id: str,
        result: str,
        points: int = 0
    ) -> Dict[str, Any]:
        """Process an agent's task completion."""
        completion_data = {
            "agent_id": agent_id,
            "task_id": task_id,
            "result": result,
            "points": points,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        # Update agent status
        self._update_agent_status(agent_id, task_id, points)
        
        # Log to swarm brain
        self._log_to_swarm_brain(completion_data)
        
        return {
            "success": True,
            "completion_id": f"{agent_id}_{task_id}_{datetime.now().strftime('%Y%m%d')}",
            "points_awarded": points
        }
    
    def _update_agent_status(self, agent_id: str, task_id: str, points: int):
        """Update agent's status.json with completion."""
        status_file = Path(f"agent_workspaces/{agent_id}/status.json")
        
        if status_file.exists():
            with open(status_file, 'r') as f:
                status = json.load(f)
            
            # Move task to completed
            if 'completed_tasks' not in status:
                status['completed_tasks'] = []
            
            status['completed_tasks'].insert(0, f"{task_id}: COMPLETE (+{points} pts)")
            status['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
    
    def _log_to_swarm_brain(self, completion_data: Dict):
        """Log completion to swarm brain."""
        try:
            from src.swarm_brain.swarm_memory import SwarmMemory
            memory = SwarmMemory(agent_id='Captain')
            memory.share_learning(
                title=f"Task Completion: {completion_data['task_id']}",
                content=f"Agent {completion_data['agent_id']} completed with {completion_data['points']} points",
                tags=['completion', 'captain', 'tracking']
            )
        except Exception as e:
            print(f"Warning: Could not log to swarm brain: {e}")


class LeaderboardUpdater:
    """
    Update agent leaderboard with points and achievements.
    
    Migrated from: tools/captain_leaderboard_update.py
    """
    
    def update_leaderboard(
        self,
        agent_id: str,
        points: int,
        achievement: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update leaderboard with new points/achievement."""
        leaderboard_file = Path("agent_workspaces/leaderboard.json")
        
        # Load or create leaderboard
        if leaderboard_file.exists():
            with open(leaderboard_file, 'r') as f:
                leaderboard = json.load(f)
        else:
            leaderboard = {"agents": {}, "last_updated": None}
        
        # Update agent entry
        if agent_id not in leaderboard["agents"]:
            leaderboard["agents"][agent_id] = {
                "total_points": 0,
                "achievements": []
            }
        
        leaderboard["agents"][agent_id]["total_points"] += points
        
        if achievement:
            leaderboard["agents"][agent_id]["achievements"].append({
                "achievement": achievement,
                "points": points,
                "timestamp": datetime.now().isoformat()
            })
        
        leaderboard["last_updated"] = datetime.now().isoformat()
        
        # Save leaderboard
        with open(leaderboard_file, 'w') as f:
            json.dump(leaderboard, f, indent=2)
        
        return {
            "success": True,
            "agent_id": agent_id,
            "new_total": leaderboard["agents"][agent_id]["total_points"]
        }


class NextTaskPicker:
    """
    Pick next optimal task for an agent based on specialty and ROI.
    
    Migrated from: tools/captain_next_task_picker.py
    """
    
    def pick_next_task(
        self,
        agent_id: str,
        agent_specialty: str,
        available_tasks: List[Dict]
    ) -> Optional[Dict]:
        """Pick optimal next task for agent."""
        if not available_tasks:
            return None
        
        # Score tasks by fit to agent specialty
        scored_tasks = []
        for task in available_tasks:
            score = self._calculate_task_fit(
                agent_specialty=agent_specialty,
                task_category=task.get('category', ''),
                task_priority=task.get('priority', 'normal'),
                task_points=task.get('points', 0)
            )
            scored_tasks.append((score, task))
        
        # Sort by score (highest first)
        scored_tasks.sort(key=lambda x: x[0], reverse=True)
        
        # Return best fit
        return scored_tasks[0][1] if scored_tasks else None
    
    def _calculate_task_fit(
        self,
        agent_specialty: str,
        task_category: str,
        task_priority: str,
        task_points: int
    ) -> float:
        """Calculate how well task fits agent."""
        score = 0.0
        
        # Specialty match (+50 points)
        if agent_specialty.lower() in task_category.lower():
            score += 50.0
        
        # Priority bonus (+30 urgent, +15 high)
        if task_priority == 'urgent':
            score += 30.0
        elif task_priority == 'high':
            score += 15.0
        
        # Points ROI (+points/100)
        score += task_points / 100.0
        
        return score


class ROIQuickCalculator:
    """
    Quick ROI calculation for captain decision-making.
    
    Migrated from: tools/captain_roi_quick_calc.py
    """
    
    def calculate_roi(
        self,
        points: int,
        effort_hours: float,
        complexity: int = 5
    ) -> Dict[str, Any]:
        """Calculate ROI for a task."""
        # Base ROI: points per hour
        base_roi = points / effort_hours if effort_hours > 0 else 0
        
        # Complexity adjustment (lower complexity = higher ROI)
        complexity_factor = (10 - complexity) / 10.0
        adjusted_roi = base_roi * (1 + complexity_factor)
        
        # ROI tier
        if adjusted_roi >= 100:
            tier = "EXCELLENT"
        elif adjusted_roi >= 50:
            tier = "HIGH"
        elif adjusted_roi >= 20:
            tier = "MEDIUM"
        else:
            tier = "LOW"
        
        return {
            "base_roi": round(base_roi, 2),
            "adjusted_roi": round(adjusted_roi, 2),
            "tier": tier,
            "points": points,
            "effort_hours": effort_hours,
            "complexity": complexity
        }


# Tool registry entries
CAPTAIN_COORDINATION_TOOLS = [
    CaptainTool(
        name="captain.process_completion",
        description="Process agent task completion and award points",
        category="captain.coordination"
    ),
    CaptainTool(
        name="captain.update_leaderboard",
        description="Update agent leaderboard with points/achievements",
        category="captain.coordination"
    ),
    CaptainTool(
        name="captain.pick_next_task",
        description="Pick optimal next task for agent based on specialty/ROI",
        category="captain.coordination"
    ),
    CaptainTool(
        name="captain.calculate_roi",
        description="Quick ROI calculation for decision-making",
        category="captain.coordination"
    ),
]


def get_tools() -> List[CaptainTool]:
    """Get all captain coordination tools."""
    return CAPTAIN_COORDINATION_TOOLS

