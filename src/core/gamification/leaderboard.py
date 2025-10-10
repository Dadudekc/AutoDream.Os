#!/usr/bin/env python3
"""
Leaderboard System for Autonomous Competition
===========================================

Leaderboard display and ranking management.

Author: Captain Agent-4 (C-055-4 V2 Refactoring)
License: MIT
"""

from typing import List
from .achievements import AgentScore


class LeaderboardManager:
    """Manages leaderboard rankings and display."""
    
    @staticmethod
    def update_ranks(scores: dict) -> None:
        """Update agent ranks based on total points."""
        sorted_agents = sorted(
            scores.values(),
            key=lambda x: x.total_points,
            reverse=True
        )
        
        for rank, agent_score in enumerate(sorted_agents, start=1):
            agent_score.rank = rank
    
    @staticmethod
    def get_leaderboard(scores: dict, top_n: int = 10) -> List[AgentScore]:
        """
        Get leaderboard rankings.
        
        Args:
            scores: Dictionary of agent scores
            top_n: Number of top agents to return
            
        Returns:
            List of agent scores sorted by rank
        """
        sorted_scores = sorted(
            scores.values(),
            key=lambda x: x.total_points,
            reverse=True
        )
        return sorted_scores[:top_n]
    
    @staticmethod
    def generate_leaderboard_message(scores: dict, show_top: int = 5) -> str:
        """
        Generate leaderboard message for broadcast.
        
        Args:
            scores: Dictionary of agent scores
            show_top: Number of top agents to show
            
        Returns:
            Formatted leaderboard message
        """
        leaderboard = LeaderboardManager.get_leaderboard(scores, show_top)
        
        if not leaderboard:
            return "📊 Leaderboard: No scores yet. Start earning achievements!"
        
        lines = ["📊 AUTONOMOUS DEVELOPMENT LEADERBOARD:"]
        lines.append("")
        
        medals = ["🥇", "🥈", "🥉", "⭐", "⭐"]
        
        for i, score in enumerate(leaderboard):
            medal = medals[i] if i < len(medals) else "•"
            lines.append(
                f"{medal} #{score.rank} {score.agent_name}: "
                f"{score.total_points:,} pts "
                f"({score.proactive_count} proactive)"
            )
        
        return "\n".join(lines)


