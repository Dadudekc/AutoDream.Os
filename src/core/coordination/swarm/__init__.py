#!/usr/bin/env python3
"""
Swarm Coordination Package - V2 Compliance
==========================================

Modular swarm coordination enhancement system with V2 compliance.
Replaces the monolithic swarm_coordination_enhancer.py.

Package Structure:
- coordination_models.py: Data models and configuration
- swarm_coordination_orchestrator.py: Main orchestrator and unified interface

V2 Compliance: Modular design, single responsibility, dependency injection.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
Original: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

# Import main classes for easy access
from .coordination_models import (
    CoordinationConfig,
    CoordinationTask,
    CoordinationResult,
    CoordinationMetrics,
    CoordinationStrategy,
    CoordinationPriority,
    CoordinationStatus,
    create_default_config,
    create_coordination_task,
    create_coordination_result,
    create_coordination_metrics,
    DEFAULT_COORDINATION_STRATEGIES,
    PRIORITY_WEIGHTS,
    STRATEGY_TIMEOUTS
)

from .swarm_coordination_orchestrator import (
    SwarmCoordinationEnhancer,
    get_swarm_coordination_enhancer
)

# Package metadata
__version__ = "2.0.0"
__author__ = "Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager"
__description__ = "Modular swarm coordination enhancement system with V2 compliance"

# Export main interface functions
__all__ = [
    # Core classes
    "SwarmCoordinationEnhancer",
    
    # Data models
    "CoordinationConfig",
    "CoordinationTask",
    "CoordinationResult",
    "CoordinationMetrics",
    
    # Enums
    "CoordinationStrategy",
    "CoordinationPriority",
    "CoordinationStatus",
    
    # Factory functions
    "create_default_config",
    "create_coordination_task",
    "create_coordination_result",
    "create_coordination_metrics",
    
    # Constants
    "DEFAULT_COORDINATION_STRATEGIES",
    "PRIORITY_WEIGHTS",
    "STRATEGY_TIMEOUTS",
    
    # Main interface functions
    "get_swarm_coordination_enhancer"
]
