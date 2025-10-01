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
from .watchdog import (
    EnforcementMode,
    IntegratedWatchdog,
    MemoryWatchdog,
    WatchdogAlert,
    WatchdogManager,
)
from .report import (
    MemoryReport,
    PerformanceReporter,
    ReportFormatter,
    ReportGenerator,
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
    # Watchdog
    "EnforcementMode",
    "WatchdogAlert",
    "MemoryWatchdog",
    "IntegratedWatchdog",
    "WatchdogManager",
    # Report
    "MemoryReport",
    "ReportGenerator",
    "ReportFormatter",
    "PerformanceReporter",
]

