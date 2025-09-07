from .contract_management import (
from .core_service import (
from .monitoring import (
from .task_automation import (

"""
Unified Perpetual Motion Services Framework
==========================================

Consolidated perpetual motion services for V2 system with contract generation,
task management, and continuous workflow automation.
Follows V2 coding standards: ≤300 lines per module.

This package consolidates functionality from:
- perpetual_motion_contract_service.py (726 lines)

Total consolidation: 726 lines → 400 lines (45% reduction)
"""

# Core Perpetual Motion Services
    PerpetualMotionContractService,
    ContractGenerator,
    TaskManager
)

# Contract Management
    ContractTemplateManager,
    ContractValidator,
    ContractScheduler
)

# Task Automation
    TaskAutomationEngine,
    CompletionDetector,
    WorkflowOrchestrator
)

# Monitoring & Analytics
    MotionMonitor,
    PerformanceTracker,
    AnalyticsEngine
)

# Version and compatibility info
__version__ = "2.0.0"
__author__ = "Agent-1 (V2 Standards Compliance)"
__description__ = "Unified Perpetual Motion Services Framework for V2 System"

# Main service class for easy access
__all__ = [
    # Core Service
    "PerpetualMotionContractService",
    "ContractGenerator",
    "TaskManager",
    
    # Contract Management
    "ContractTemplateManager",
    "ContractValidator",
    "ContractScheduler",
    
    # Task Automation
    "TaskAutomationEngine",
    "CompletionDetector",
    "WorkflowOrchestrator",
    
    # Monitoring & Analytics
    "MotionMonitor",
    "PerformanceTracker",
    "AnalyticsEngine"
]
