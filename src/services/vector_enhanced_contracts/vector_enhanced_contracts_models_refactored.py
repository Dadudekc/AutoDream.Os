#!/usr/bin/env python3
"""
Vector Enhanced Contracts Models Refactored - V2 Compliance Module
==================================================================

Main refactored entry point for vector enhanced contracts models.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# Import enums
from .vector_enhanced_contracts_enums import (
    ContractStatus,
    PriorityLevel,
    TaskType,
    AssignmentStrategy
)

# Import core models
from .vector_enhanced_contracts_models_core import (
    AgentCapability,
    TaskRecommendation,
    ContractAssignment
)

# Import extended models
from .vector_enhanced_contracts_models_extended import (
    PerformanceMetrics,
    PerformanceTrend,
    OptimizationResult
)

# Re-export all models for backward compatibility
__all__ = [
    # Enums
    "ContractStatus",
    "PriorityLevel", 
    "TaskType",
    "AssignmentStrategy",
    
    # Core models
    "AgentCapability",
    "TaskRecommendation",
    "ContractAssignment",
    
    # Extended models
    "PerformanceMetrics",
    "PerformanceTrend",
    "OptimizationResult"
]
