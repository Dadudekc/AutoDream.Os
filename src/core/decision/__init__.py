#!/usr/bin/env python3
"""
Decision System - Agent Cellphone V2
====================================

Modular decision-making system with algorithms, workflows, and rules.
Follows V2 standards: SRP, OOP design, modular architecture.

Author: Agent-1 (Integration & Core Systems)
License: MIT
"""

# Core decision system
from .decision_core import DecisionCore, DecisionCoreConfig

# Specialized components
from .decision_algorithms import DecisionAlgorithmExecutor, AlgorithmPerformance
from .decision_workflows import DecisionWorkflowExecutor, WorkflowStep, WorkflowExecution
from .decision_rules import DecisionRuleEngine, RuleEvaluationResult, RulePerformance

# Main decision manager (orchestrates all components)
from .decision_manager import DecisionManager, DecisionManagerConfig

# Models and types
from .decision_types import (
    DecisionRequest, DecisionResult, DecisionContext, DecisionType,
    DecisionPriority, DecisionStatus, DecisionConfidence, IntelligenceLevel,
    DecisionMetrics  # SSOT: Unified decision metrics
)

# Factory functions for easy component creation
def create_decision_core(manager_id: str, name: str = "Decision Core", description: str = "") -> DecisionCore:
    """Create a new decision core instance."""
    return DecisionCore(manager_id, name, description)

def create_decision_manager(manager_id: str, name: str = "Decision Manager", description: str = "") -> DecisionManager:
    """Create a new decision manager instance."""
    return DecisionManager(manager_id, name, description)

def create_algorithm_executor() -> DecisionAlgorithmExecutor:
    """Create a new algorithm executor instance."""
    return DecisionAlgorithmExecutor()

def create_workflow_executor() -> DecisionWorkflowExecutor:
    """Create a new workflow executor instance."""
    return DecisionWorkflowExecutor()

def create_rule_engine() -> DecisionRuleEngine:
    """Create a new rule engine instance."""
    return DecisionRuleEngine()

# Backward compatibility aliases
DecisionCoreV2 = DecisionCore
DecisionAlgorithmManager = DecisionAlgorithmExecutor
DecisionWorkflowManager = DecisionWorkflowExecutor
DecisionRuleManager = DecisionRuleEngine

# Export all components
__all__ = [
    # Core system
    "DecisionCore",
    "DecisionCoreConfig",
    "DecisionManager",
    "DecisionManagerConfig",
    
    # Specialized components
    "DecisionAlgorithmExecutor",
    "DecisionWorkflowExecutor",
    "DecisionRuleEngine",
    "AlgorithmPerformance",
    "WorkflowStep",
    "WorkflowExecution",
    "RuleEvaluationResult",
    "RulePerformance",
    
    # Models and types
    "DecisionRequest",
    "DecisionResult",
    "DecisionContext",
    "DecisionType",
    "DecisionPriority",
    "DecisionStatus",
    "DecisionConfidence",
    "IntelligenceLevel",
    "DecisionMetrics",
    
    # Factory functions
    "create_decision_core",
    "create_decision_manager",
    "create_algorithm_executor",
    "create_workflow_executor",
    "create_rule_engine",
    
    # Backward compatibility
    "DecisionCoreV2",
    "DecisionAlgorithmManager",
    "DecisionWorkflowManager",
    "DecisionRuleManager"
]
