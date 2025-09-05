#!/usr/bin/env python3
"""
Messaging Protocol Package - V2 Compliance
==========================================

Modular messaging protocol optimization system with V2 compliance.
Replaces the monolithic messaging_protocol_optimizer.py.

Package Structure:
- messaging_protocol_models.py: Data models and configuration
- messaging_protocol_router.py: Intelligent routing and optimization
- messaging_protocol_batch_manager.py: Batching and queue management
- messaging_protocol_orchestrator.py: Main orchestrator and unified interface

V2 Compliance: Modular design, single responsibility, dependency injection.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
Original: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

# Import main classes for easy access
from .messaging_protocol_models import (
    OptimizationConfig,
    ProtocolMetrics,
    MessageBatch,
    RouteOptimization,
    DeliveryResult,
    ProtocolOptimizationStrategy,
    MessageRoute,
    create_default_config,
    create_message_batch,
    create_route_optimization,
    create_delivery_result,
    DEFAULT_OPTIMIZATION_STRATEGIES,
    ROUTE_PRIORITY_ORDER
)

from .messaging_protocol_router import MessagingProtocolRouter

from .messaging_protocol_batch_manager import MessagingProtocolBatchManager

from .messaging_protocol_orchestrator import (
    MessagingProtocolOrchestrator,
    get_messaging_protocol_optimizer,
    MessagingProtocolOptimizer
)

# Package metadata
__version__ = "2.0.0"
__author__ = "Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager"
__description__ = "Modular messaging protocol optimization system with V2 compliance"

# Export main interface functions
__all__ = [
    # Core classes
    "MessagingProtocolOrchestrator",
    "MessagingProtocolRouter",
    "MessagingProtocolBatchManager",
    
    # Data models
    "OptimizationConfig",
    "ProtocolMetrics",
    "MessageBatch",
    "RouteOptimization",
    "DeliveryResult",
    
    # Enums
    "ProtocolOptimizationStrategy",
    "MessageRoute",
    
    # Factory functions
    "create_default_config",
    "create_message_batch",
    "create_route_optimization",
    "create_delivery_result",
    
    # Constants
    "DEFAULT_OPTIMIZATION_STRATEGIES",
    "ROUTE_PRIORITY_ORDER",
    
    # Main interface functions
    "get_messaging_protocol_optimizer",
    
    # Backward compatibility
    "MessagingProtocolOptimizer"
]
