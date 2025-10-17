"""
Autonomous Task Engine - Backward Compatible Facade
==================================================
V2-compliant facade for autonomous_task_engine package.

REFACTORED: 2025-10-16 by Agent-2 (Architecture & Design Specialist)
Original: 781 lines → Modular: 4 files <400L each

This facade maintains 100% backward compatibility while delegating to modular implementation.

Usage (unchanged):
    from tools.autonomous_task_engine import AutonomousTaskEngine
    
    engine = AutonomousTaskEngine()
    task = engine.get_optimal_task_for_agent("Agent-2")

Modular Structure:
    tools/autonomous_task_engine/
    ├── models.py (69L) - Task, AgentProfile, TaskRecommendation
    ├── discovery.py (257L) - Task discovery methods
    ├── scoring.py (224L) - Task scoring & recommendations
    ├── engine.py (270L) - Core engine orchestration
    └── cli.py (106L) - Command-line interface

V2 Compliance: ✅ All modules <400 lines
Backward Compatibility: ✅ 100% maintained
"""

# Import from modular implementation
from .autonomous_task_engine import (
    Task,
    AgentProfile,
    TaskRecommendation,
    AutonomousTaskEngine,
    TaskDiscovery,
    TaskScoring,
)

# Re-export for backward compatibility
__all__ = [
    "Task",
    "AgentProfile",
    "TaskRecommendation",
    "AutonomousTaskEngine",
    "TaskDiscovery",
    "TaskScoring",
]


# CLI entry point
if __name__ == "__main__":
    from .autonomous_task_engine.cli import main
    main()
