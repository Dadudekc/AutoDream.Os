#!/usr/bin/env python3
"""
Vector Enhanced Contracts Package - V2 Compliance Module
=======================================================

Modular vector enhanced contracts system for V2 compliance.
Replaces monolithic vector_enhanced_contracts.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .vector_enhanced_contracts_models import (
    ContractAssignment,
    TaskRecommendation,
    PerformanceMetrics,
    AgentCapability,
    ContractStatus,
    PriorityLevel,
    TaskType,
    AssignmentStrategy,
    PerformanceTrend,
    OptimizationResult,
)
from .vector_enhanced_contracts_engine import VectorEnhancedContractEngine
from .vector_enhanced_contracts_orchestrator import (
    VectorEnhancedContractService,
    get_vector_enhanced_contract_service,
    get_optimal_task_assignment,
    track_contract_progress,
    analyze_performance_patterns,
    optimize_agent_assignments,
    get_contract_recommendations,
    update_agent_capabilities,
    get_performance_metrics,
    get_contract_analytics,
)

__all__ = [
    'ContractAssignment',
    'TaskRecommendation',
    'PerformanceMetrics',
    'AgentCapability',
    'ContractStatus',
    'PriorityLevel',
    'TaskType',
    'AssignmentStrategy',
    'PerformanceTrend',
    'OptimizationResult',
    'VectorEnhancedContractEngine',
    'VectorEnhancedContractService',
    'get_vector_enhanced_contract_service',
    'get_optimal_task_assignment',
    'track_contract_progress',
    'analyze_performance_patterns',
    'optimize_agent_assignments',
    'get_contract_recommendations',
    'update_agent_capabilities',
    'get_performance_metrics',
    'get_contract_analytics',
]
