"""
Overnight Autonomous Runner - V2 Compliant
==========================================

24/7 autonomous execution system for continuous agent operations.
Extends V2's orchestration framework with cycle-based scheduling and recovery.

V2 Compliance: All files ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Autonomous Operations Specialist
License: MIT
"""

from .orchestrator import OvernightOrchestrator
from .scheduler import TaskScheduler
from .monitor import ProgressMonitor
from .recovery import RecoverySystem

__all__ = [
    'OvernightOrchestrator',
    'TaskScheduler',
    'ProgressMonitor',
    'RecoverySystem',
]

__version__ = "2.0.0"
__author__ = "Agent-1 - Autonomous Operations Specialist"
