"""
Autonomous Task Engine - Core Engine
====================================
Main engine class orchestrating task discovery, scoring, and management.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-10-16
License: MIT
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import asdict
from datetime import datetime

from .models import Task, AgentProfile, TaskRecommendation
from .discovery import TaskDiscovery
from .scoring import TaskScoring


class AutonomousTaskEngine:
    """
    The Masterpiece Tool - Autonomous Task Discovery & Selection Engine
    
    Enables agents to:
    1. Discover optimal tasks autonomously
    2. Get personalized recommendations based on skills
    3. Calculate ROI and impact automatically
    4. Claim and track tasks without Captain intervention
    5. Coordinate with other agents intelligently
    """
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.tasks_db_path = Path("runtime/autonomous_tasks.json")
        self.tasks: List[Task] = []
        self.agent_profiles: Dict[str, AgentProfile] = {}
        
        # Initialize components
        self.discovery = TaskDiscovery(self.repo_path)
        self.scoring = TaskScoring(self.agent_profiles)
        
        # Load persistent data
        self._load_tasks()
        self._load_agent_profiles()
    
    def discover_tasks(self) -> List[Task]:
        """
        Scan codebase and discover ALL available task opportunities
        
        This is the heart of autonomous intelligence - finding work
        """
        discovered = self.discovery.discover_all()
        
        # Calculate skill match for all agents
        for task in discovered:
            task.skill_match = self.scoring.calculate_skill_matches(task)
        
        self.tasks = discovered
        self._save_tasks()
        
        return discovered
    
    def get_optimal_task_for_agent(
        self,
        agent_id: str,
        exclude_types: Optional[List[str]] = None,
        min_roi: float = 0.0
    ) -> Optional[TaskRecommendation]:
        """
        Get the BEST task for a specific agent
        
        This is THE function that enables autonomous agent work selection
        """
        if not self.tasks:
            self.discover_tasks()
        
        return self.scoring.get_optimal_task(
            self.tasks, agent_id, exclude_types, min_roi
        )
    
    def get_top_n_tasks_for_agent(
        self,
        agent_id: str,
        n: int = 5
    ) -> List[TaskRecommendation]:
        """Get top N task recommendations for agent"""
        if not self.tasks:
            self.discover_tasks()
        
        return self.scoring.get_top_n_tasks(self.tasks, agent_id, n)
    
    def claim_task(
        self,
        task_id: str,
        agent_id: str
    ) -> bool:
        """Claim a task for an agent"""
        task = self._find_task(task_id)
        if not task:
            return False
        
        if task.claimed_by is not None:
            return False
        
        task.claimed_by = agent_id
        task.claimed_at = datetime.now()
        task.status = "CLAIMED"
        
        self._save_tasks()
        return True
    
    def start_task(self, task_id: str, agent_id: str) -> bool:
        """Mark task as in progress"""
        task = self._find_task(task_id)
        if not task or task.claimed_by != agent_id:
            return False
        
        task.status = "IN_PROGRESS"
        self._save_tasks()
        return True
    
    def complete_task(
        self,
        task_id: str,
        agent_id: str,
        actual_effort: int,
        actual_points: int
    ) -> bool:
        """Mark task as complete and update agent profile"""
        task = self._find_task(task_id)
        if not task or task.claimed_by != agent_id:
            return False
        
        task.status = "COMPLETED"
        self._save_tasks()
        
        # Update agent profile
        self._update_agent_profile(
            agent_id, task.task_type, actual_effort, actual_points
        )
        
        return True
    
    def generate_autonomous_report(self, agent_id: str) -> str:
        """Generate a report for autonomous agent use"""
        from datetime import datetime
        
        recommendations = self.get_top_n_tasks_for_agent(agent_id, n=5)
        
        if not recommendations:
            return f"No tasks available for {agent_id}. Consider discovering new tasks."
        
        report = []
        report.append("=" * 80)
        report.append(f"AUTONOMOUS TASK RECOMMENDATIONS FOR {agent_id}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        for i, rec in enumerate(recommendations, 1):
            task = rec.task
            report.append(f"#{i} RECOMMENDATION (Score: {rec.total_score:.2f})")
            report.append(f"Task ID: {task.task_id}")
            report.append(f"Title: {task.title}")
            report.append(f"Type: {task.task_type} | Severity: {task.severity}")
            report.append(f"File: {task.file_path}")
            report.append(f"Effort: {task.estimated_effort} cycles | Points: {task.estimated_points}")
            report.append(f"ROI: {task.roi_score:.2f} | Impact: {task.impact_score:.1f}/10")
            
            if task.current_lines and task.target_lines:
                report.append(
                    f"Lines: {task.current_lines}→{task.target_lines} "
                    f"({task.reduction_percent:.0f}% reduction)"
                )
            
            report.append(f"Match Score: {rec.match_score:.2f} | Priority: {rec.priority_score:.2f}")
            report.append("")
            report.append("WHY THIS TASK:")
            for reason in rec.reasoning:
                report.append(f"  ✓ {reason}")
            report.append("")
            
            if rec.pros:
                report.append("PROS:")
                for pro in rec.pros:
                    report.append(f"  + {pro}")
                report.append("")
            
            if rec.cons:
                report.append("CONS:")
                for con in rec.cons:
                    report.append(f"  - {con}")
                report.append("")
            
            report.append(f"SUGGESTED APPROACH: {rec.suggested_approach}")
            
            if rec.coordination_plan:
                report.append(f"COORDINATION: {rec.coordination_plan}")
            
            report.append("")
            report.append(
                f"TO CLAIM: python tools/autonomous_task_engine.py "
                f"--claim {task.task_id} --agent {agent_id}"
            )
            report.append("-" * 80)
            report.append("")
        
        return "\n".join(report)
    
    # === PRIVATE METHODS ===
    
    def _find_task(self, task_id: str) -> Optional[Task]:
        """Find task by ID"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def _update_agent_profile(
        self,
        agent_id: str,
        task_type: str,
        effort: int,
        points: int
    ):
        """Update agent profile after task completion"""
        profile = self.scoring._get_or_create_agent_profile(agent_id)
        
        if task_type not in profile.past_work_types:
            profile.past_work_types[task_type] = 0
        profile.past_work_types[task_type] += 1
        
        profile.total_points += points
        
        self._save_agent_profiles()
    
    def _load_tasks(self):
        """Load tasks from disk"""
        if self.tasks_db_path.exists():
            try:
                with open(self.tasks_db_path) as f:
                    data = json.load(f)
                    self.tasks = [Task(**t) for t in data]
            except Exception:
                self.tasks = []
    
    def _save_tasks(self):
        """Save tasks to disk"""
        self.tasks_db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tasks_db_path, "w") as f:
            json.dump([asdict(t) for t in self.tasks], f, indent=2, default=str)
    
    def _load_agent_profiles(self):
        """Load agent profiles"""
        profiles_path = Path("runtime/agent_profiles.json")
        if profiles_path.exists():
            try:
                with open(profiles_path) as f:
                    data = json.load(f)
                    self.agent_profiles = {
                        k: AgentProfile(**v) for k, v in data.items()
                    }
                    # Update scoring component with loaded profiles
                    self.scoring.agent_profiles = self.agent_profiles
            except Exception:
                pass
    
    def _save_agent_profiles(self):
        """Save agent profiles"""
        profiles_path = Path("runtime/agent_profiles.json")
        profiles_path.parent.mkdir(parents=True, exist_ok=True)
        with open(profiles_path, "w") as f:
            json.dump(
                {k: asdict(v) for k, v in self.agent_profiles.items()},
                f, indent=2, default=str
            )

