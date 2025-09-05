#!/usr/bin/env python3
"""
Vector Enhanced Contracts Models - V2 Compliance Module
======================================================

Backward compatibility wrapper for vector enhanced contracts models.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

# Import all models from refactored modules
from .vector_enhanced_contracts_models_refactored import *

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
