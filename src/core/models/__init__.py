"""
Unified Model Framework - Agent Cellphone V2

Provides a comprehensive, unified model system that consolidates
all scattered model and enum implementations across the codebase.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3J - Model & Enum Consolidation
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

from .unified_model_framework import (
    UnifiedModelFramework,
    UnifiedStatus,
    UnifiedPriority,
    UnifiedSeverity,
    UnifiedType,
    UnifiedFormat,
    BaseModel,
    StatusModel,
    TypedModel,
    HealthModel,
    PerformanceModel,
    TaskModel,
    WorkflowModel,
    MessageModel,
    ModelRegistry,
    UnifiedModelFactory
)

from .model_consolidation_system import (
    ModelConsolidationSystem,
    ConsolidationTarget,
    ConsolidationPlan
)

from .model_elimination_system import (
    ModelEliminationSystem,
    EliminationTarget,
    EliminationPlan
)

__all__ = [
    # Core framework
    'UnifiedModelFramework',
    'UnifiedStatus',
    'UnifiedPriority',
    'UnifiedSeverity',
    'UnifiedType',
    'UnifiedFormat',
    
    # Base models
    'BaseModel',
    'StatusModel',
    'TypedModel',
    
    # Specialized models
    'HealthModel',
    'PerformanceModel',
    'TaskModel',
    'WorkflowModel',
    'MessageModel',
    
    # Registry and factory
    'ModelRegistry',
    'UnifiedModelFactory',
    
    # System consolidation
    'ModelConsolidationSystem',
    'ConsolidationTarget',
    'ConsolidationPlan',
    
    # System elimination
    'ModelEliminationSystem',
    'EliminationTarget',
    'EliminationPlan'
]

