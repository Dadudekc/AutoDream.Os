"""
Gamification System for Autonomous Development
==============================================

Competition system that drives proactive agent behavior while
maintaining cooperative swarm intelligence.

Based on Captain's insight: Competition drives autonomous excellence.
"""

from .autonomous_competition_system import (
    Achievement,
    AchievementType,
    AgentScore,
    AutonomousCompetitionSystem,
    CompetitionMode,
    LeaderboardManager,
    ScoringCalculator,
    get_competition_system,
)

__all__ = [
    "AutonomousCompetitionSystem",
    "Achievement",
    "AchievementType",
    "AgentScore",
    "CompetitionMode",
    "get_competition_system",
    "ScoringCalculator",
    "LeaderboardManager",
]
