#!/usr/bin/env python3
"""
Competition System Core
===========================================

Core autonomous competition system functionality.

Author: Captain Agent-4 (C-055-4 V2 Refactoring)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

from .achievements import Achievement, AchievementType, AgentScore, ScoringCalculator
from .leaderboard import LeaderboardManager
from .competition_storage import load_scores, save_scores, update_ranks


class CompetitionMode(Enum):
    """Competition modes for different scenarios."""
    
    COOPERATIVE = "cooperative"  # Default: Team-based, celebrate together
    FRIENDLY = "friendly"  # Leaderboard visible, collaborative spirit
    SPRINT = "sprint"  # Time-boxed competitive sprints
    AUTONOMOUS = "autonomous"  # Encourage proactive self-direction


class AutonomousCompetitionSystem:
    """
    Gamification system for autonomous development.
    
    Encourages proactive behavior through:
    - Point-based achievements
    - Leaderboards (optional display)
    - Proactive initiative bonuses
    - Quality multipliers
    - Collaboration rewards
    """
    
    def __init__(
        self,
        mode: CompetitionMode = CompetitionMode.AUTONOMOUS,
        storage_path: str = "runtime/competition"
    ):
        """Initialize competition system."""
        self.mode = mode
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.scores: Dict[str, AgentScore] = {}
        self.achievements: List[Achievement] = []
        
        # Load existing scores
        self.scores = load_scores(self.storage_path)
    
    def award_achievement(
        self,
        agent_id: str,
        agent_name: str,
        achievement_type: AchievementType,
        title: str,
        description: str,
        points: int,
        mission_ref: Optional[str] = None,
        evidence: List[str] = None,
        is_proactive: bool = False,
        quality_metrics: Dict[str, float] = None
    ) -> Achievement:
        """
        Award achievement to agent.
        
        Args:
            agent_id: Agent identifier
            agent_name: Agent display name
            achievement_type: Type of achievement
            title: Achievement title
            description: Achievement description
            points: Points awarded
            mission_ref: Related mission/cycle reference
            evidence: Evidence of achievement
            is_proactive: Whether this was proactive work
            quality_metrics: Quality metrics for multiplier
            
        Returns:
            Achievement instance
        """
        # Calculate final points with multipliers
        final_points = points
        
        if is_proactive:
            final_points = ScoringCalculator.calculate_proactive_bonus(points)
        
        if quality_metrics:
            multiplier = ScoringCalculator.calculate_quality_multiplier(quality_metrics)
            final_points = int(final_points * multiplier)
        
        achievement_id = f"{agent_id}_{len(self.achievements)}_{int(datetime.now().timestamp())}"
        
        achievement = Achievement(
            achievement_id=achievement_id,
            agent_id=agent_id,
            achievement_type=achievement_type,
            title=title,
            description=description,
            points=final_points,
            timestamp=datetime.now().isoformat(),
            mission_ref=mission_ref,
            evidence=evidence or [],
            metadata={
                "is_proactive": is_proactive,
                "quality_metrics": quality_metrics or {},
                "base_points": points
            }
        )
        
        self.achievements.append(achievement)
        
        # Update agent score
        if agent_id not in self.scores:
            self.scores[agent_id] = AgentScore(
                agent_id=agent_id,
                agent_name=agent_name,
                total_points=0
            )
        
        agent_score = self.scores[agent_id]
        agent_score.total_points += final_points
        agent_score.achievements.append(achievement)
        agent_score.last_updated = datetime.now().isoformat()
        
        if is_proactive:
            agent_score.proactive_count += 1
        
        # Update ranks
        LeaderboardManager.update_ranks(self.scores)
        
        # Persist
        save_scores(self.storage_path, self.scores)
        
        return achievement
    
    def get_leaderboard(self, top_n: int = 10) -> List[AgentScore]:
        """Get leaderboard rankings."""
        return LeaderboardManager.get_leaderboard(self.scores, top_n)
    
    def get_agent_score(self, agent_id: str) -> Optional[AgentScore]:
        """Get specific agent's score."""
        return self.scores.get(agent_id)
    
    def generate_leaderboard_message(self, show_top: int = 5) -> str:
        """Generate leaderboard message."""
        return LeaderboardManager.generate_leaderboard_message(self.scores, show_top)


# Global singleton
_competition_system = None


def get_competition_system() -> AutonomousCompetitionSystem:
    """Get global competition system instance."""
    global _competition_system
    if _competition_system is None:
        _competition_system = AutonomousCompetitionSystem()
    return _competition_system


