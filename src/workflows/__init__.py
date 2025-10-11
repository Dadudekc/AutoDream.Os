"""
Advanced Workflows System - V2 Compliant
========================================

Production-grade workflow orchestration for multi-agent coordination.
Built on V2's messaging and coordinate infrastructure.

V2 Compliance: All files ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Workflow Orchestration Specialist
License: MIT
"""

from .engine import WorkflowEngine
from .models import AIResponse, WorkflowProgress, WorkflowState, WorkflowStep
from .steps import (
    AutonomousLoopBuilder,
    ConversationLoopBuilder,
    DecisionTreeBuilder,
    MultiAgentOrchestrationBuilder,
    WorkflowStepBuilder,
)
from .strategies import (
    DecisionTreeStrategy,
    ParallelStrategy,
    SequentialStrategy,
)
from .autonomous_strategy import AutonomousStrategy

__all__ = [
    # Models
    "WorkflowState",
    "WorkflowStep",
    "AIResponse",
    "WorkflowProgress",
    # Engine
    "WorkflowEngine",
    # Step Builders
    "WorkflowStepBuilder",
    "ConversationLoopBuilder",
    "MultiAgentOrchestrationBuilder",
    "DecisionTreeBuilder",
    "AutonomousLoopBuilder",
    # Strategies
    "ParallelStrategy",
    "SequentialStrategy",
    "DecisionTreeStrategy",
    "AutonomousStrategy",
]

__version__ = "2.0.0"
__author__ = "Agent-1 - Workflow Orchestration Specialist"
