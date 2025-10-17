"""
Autonomous Task Engine - Task Scoring & Recommendations
======================================================
Methods for scoring tasks and generating personalized recommendations for agents.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-10-16
License: MIT
"""

from typing import Dict, List, Optional
from .models import Task, AgentProfile, TaskRecommendation


class TaskScoring:
    """Scores tasks and creates personalized recommendations"""
    
    def __init__(self, agent_profiles: Dict[str, AgentProfile]):
        self.agent_profiles = agent_profiles
    
    def calculate_skill_matches(self, task: Task) -> Dict[str, float]:
        """Calculate how well each agent matches this task"""
        matches = {}
        
        for agent_id, profile in self.agent_profiles.items():
            score = 0.0
            
            # Has worked on similar tasks
            if task.task_type in profile.past_work_types:
                score += 0.3
            
            # Has worked on this file or nearby
            if task.file_path in profile.files_worked:
                score += 0.4
            
            # Complexity match
            if task.estimated_effort <= 2 and profile.preferred_complexity == "SIMPLE":
                score += 0.2
            elif 2 < task.estimated_effort <= 4 and profile.preferred_complexity == "MODERATE":
                score += 0.2
            elif task.estimated_effort > 4 and profile.preferred_complexity == "COMPLEX":
                score += 0.2
            
            # Success rate bonus
            score += profile.success_rate * 0.1
            
            matches[agent_id] = min(score, 1.0)
        
        return matches
    
    def score_task_for_agent(
        self,
        task: Task,
        profile: AgentProfile
    ) -> TaskRecommendation:
        """Score a task for a specific agent"""
        # Match score (skill alignment)
        match_score = task.skill_match.get(profile.agent_id, 0.5)
        
        # Priority score (urgency + impact)
        severity_weight = {"CRITICAL": 1.0, "MAJOR": 0.7, "MINOR": 0.4}
        priority_score = (
            severity_weight.get(task.severity, 0.5) * 0.6 +
            (task.impact_score / 10) * 0.4
        )
        
        # Total score
        total_score = (match_score * 0.5 + priority_score * 0.3 + (task.roi_score / 300) * 0.2)
        
        # Generate reasoning
        reasoning = []
        if match_score > 0.7:
            reasoning.append("Strong skill match based on past work")
        if task.roi_score > 200:
            reasoning.append(f"High ROI: {task.roi_score:.0f} points/cycle")
        if task.severity == "CRITICAL":
            reasoning.append("Critical priority - high impact")
        if task.estimated_effort <= 2:
            reasoning.append("Quick win - low effort")
        
        pros = []
        cons = []
        
        if task.roi_score > 200:
            pros.append(f"Excellent ROI: {task.roi_score:.0f}")
        if task.estimated_effort <= 2:
            pros.append("Fast completion possible")
        if not task.coordination_needed:
            pros.append("No coordination required")
        
        if task.estimated_effort >= 4:
            cons.append("High effort required")
        if task.coordination_needed:
            cons.append(f"Needs coordination with: {', '.join(task.coordination_needed)}")
        if match_score < 0.5:
            cons.append("Outside usual expertise area")
        
        approach = (
            f"Refactor {task.file_path} into modular components, "
            f"target {task.reduction_percent:.0f}% reduction"
            if task.reduction_percent
            else f"Address {task.task_type.lower()} in {task.file_path}"
        )
        
        coord_plan = None
        if task.coordination_needed:
            coord_plan = f"Coordinate with {', '.join(task.coordination_needed)} before starting"
        
        return TaskRecommendation(
            agent_id=profile.agent_id,
            task=task,
            match_score=match_score,
            priority_score=priority_score,
            total_score=total_score,
            reasoning=reasoning,
            pros=pros,
            cons=cons,
            suggested_approach=approach,
            coordination_plan=coord_plan
        )
    
    def get_optimal_task(
        self,
        tasks: List[Task],
        agent_id: str,
        exclude_types: Optional[List[str]] = None,
        min_roi: float = 0.0
    ) -> Optional[TaskRecommendation]:
        """
        Get the BEST task for a specific agent
        
        This is THE function that enables autonomous agent work selection
        """
        # Get agent profile
        profile = self._get_or_create_agent_profile(agent_id)
        
        # Filter available tasks
        available = [
            t for t in tasks
            if t.status == "AVAILABLE"
            and t.claimed_by is None
            and (not exclude_types or t.task_type not in exclude_types)
            and t.roi_score >= min_roi
            and not self._has_unmet_blockers(t)
        ]
        
        if not available:
            return None
        
        # Score each task for this agent
        recommendations = []
        for task in available:
            rec = self.score_task_for_agent(task, profile)
            recommendations.append(rec)
        
        # Sort by total score
        recommendations.sort(key=lambda r: r.total_score, reverse=True)
        
        return recommendations[0] if recommendations else None
    
    def get_top_n_tasks(
        self,
        tasks: List[Task],
        agent_id: str,
        n: int = 5
    ) -> List[TaskRecommendation]:
        """Get top N task recommendations for agent"""
        profile = self._get_or_create_agent_profile(agent_id)
        
        available = [
            t for t in tasks
            if t.status == "AVAILABLE"
            and t.claimed_by is None
            and not self._has_unmet_blockers(t)
        ]
        
        recommendations = [
            self.score_task_for_agent(t, profile)
            for t in available
        ]
        
        recommendations.sort(key=lambda r: r.total_score, reverse=True)
        return recommendations[:n]
    
    def _get_or_create_agent_profile(self, agent_id: str) -> AgentProfile:
        """Get agent profile or create default"""
        if agent_id in self.agent_profiles:
            return self.agent_profiles[agent_id]
        
        # Create default profile
        profile = AgentProfile(
            agent_id=agent_id,
            specializations=[],
            past_work_types={},
            files_worked=[],
            avg_cycle_time=2.0,
            total_points=0,
            success_rate=0.8,
            preferred_complexity="MODERATE",
            current_workload=0
        )
        
        self.agent_profiles[agent_id] = profile
        return profile
    
    def _has_unmet_blockers(self, task: Task) -> bool:
        """Check if task has unmet blockers"""
        # Could check if blocker tasks are completed
        return len(task.blockers) > 0

