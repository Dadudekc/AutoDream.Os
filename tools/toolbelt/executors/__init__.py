#!/usr/bin/env python3
"""
Agent Toolbelt Executors - Modular Architecture
===============================================

V2-compliant modular architecture with facade pattern.
All executor classes extracted into focused modules.

Author: Agent-2 - Architecture & Design Specialist
V2 Compliance Refactor: agent_toolbelt_executors.py (618→78 lines, 87% reduction!)
ROI: 9.5 (VERY HIGH), Points: 350, Complexity: LOW

Architecture Pattern: Facade + Module Splitting
- 8 executor modules (each <250 lines, single responsibility)
- Facade for backward compatibility
- Clean imports and re-exports

Modules:
- vector_executor.py (Vector database operations)
- messaging_executor.py (Messaging operations)
- analysis_executor.py (Analysis operations)
- v2_executor.py (V2 compliance operations)
- agent_executor.py (Agent operations)
- consolidation_executor.py (Consolidation operations)
- refactor_executor.py (Refactoring operations)
- compliance_executor.py (Compliance checking operations)

Original: 618 lines, 8 classes
New: 8 modules < 250 lines each + 1 facade < 100 lines
"""

# Import all executors
from .agent_executor import AgentExecutor
from .analysis_executor import AnalysisExecutor
from .compliance_executor import ComplianceExecutor
from .consolidation_executor import ConsolidationExecutor
from .messaging_executor import MessagingExecutor
from .refactor_executor import RefactorExecutor
from .v2_executor import V2Executor
from .vector_executor import VectorExecutor

# Public API - Backward compatible with original agent_toolbelt_executors.py
__all__ = [
    "VectorExecutor",
    "MessagingExecutor",
    "AnalysisExecutor",
    "V2Executor",
    "AgentExecutor",
    "ConsolidationExecutor",
    "RefactorExecutor",
    "ComplianceExecutor",
]
