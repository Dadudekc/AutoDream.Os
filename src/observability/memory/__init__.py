"""
Memory Observability Module - V2_SWARM
======================================

Memory monitoring, leak detection, and policy enforcement.

Author: Agent-5 (Coordinator)
License: MIT
"""

from .detectors import (
    AutoCleanupManager,
    ComprehensiveLeakDetector,
    LeakDetectionResult,
    MemoryLeakDetector,
    MemoryTrend,
    ObjectLeakDetector,
)
from .ledger import (
    LedgerAnalyzer,
    LedgerEntry,
    MemoryLedger,
    PersistentLedgerManager,
)
from .policies import (
    MemoryBudget,
    MemoryPolicyEnforcer,
    MemoryPolicyLoader,
    MemoryPolicyManager,
    MemorySnapshot,
    TracemallocIntegration,
)

__all__ = [
    # Policies
    "MemoryBudget",
    "MemorySnapshot",
    "MemoryPolicyLoader",
    "TracemallocIntegration",
    "MemoryPolicyEnforcer",
    "MemoryPolicyManager",
    # Detectors
    "LeakDetectionResult",
    "MemoryTrend",
    "MemoryLeakDetector",
    "ObjectLeakDetector",
    "AutoCleanupManager",
    "ComprehensiveLeakDetector",
    # Ledger
    "LedgerEntry",
    "MemoryLedger",
    "LedgerAnalyzer",
    "PersistentLedgerManager",
]

