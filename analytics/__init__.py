"""
Analytics Module for Agent Efficiency Scoring
============================================

Automated efficiency scoring system with CI signal integration.
Replaces manual scoring in captain progress tracker.

Author: Agent-1 (Architecture Foundation Specialist)
License: MIT
"""

from .agent_metrics import DEFAULT_WEIGHTS, AgentSnapshot, Weights, efficiency_score
from .score_window import score_window
from .window_loader import load_snapshots_from_window

__all__ = [
    "AgentSnapshot",
    "efficiency_score",
    "Weights",
    "DEFAULT_WEIGHTS",
    "load_snapshots_from_window",
    "score_window",
]

__version__ = "1.0.0"
__author__ = "Agent-1"
__description__ = "Automated Agent Efficiency Scoring System"
