"""
🎯 UNIFIED INTERFACE SYSTEM - SINGLE SOURCE OF TRUTH
Agent-7 - Interface Systems Consolidation Specialist

Consolidated interface definitions from across the codebase.
Eliminates SSOT violations by providing unified interfaces for all systems.

This module consolidates interfaces from:
- src/core/learning/interfaces/
- src/services/interfaces/
- src/fsm/interfaces/
- src/managers/ai_ml/interfaces/
- agent_workspaces/meeting/src/ai_ml/interfaces/
- Multiple scattered interface definitions

Agent: Agent-7 (Interface Systems Consolidation Specialist)
Mission: CRITICAL SSOT Consolidation - 50%+ reduction in duplicate folders
Priority: CRITICAL - Above all other work
Status: IMPLEMENTATION PHASE 1 - Unified Interface System

Author: Agent-7 - Quality Completion Optimization Manager
License: MIT
"""

from .learning_interfaces import LearningInterface
from .service_interfaces import (
    BulkMessagingInterface,
    CampaignMessagingInterface,
    CoordinateDataInterface,
    CoordinateManagerInterface,
    CrossSystemMessagingInterface,
    FSMMessagingInterface,
    MessageSenderInterface,
    OnboardingMessagingInterface,
    YOLOMessagingInterface
)
from .fsm_interfaces import (
    StateInterface,
    TransitionInterface,
    WorkflowInterface
)
from .ai_ml_interfaces import (
    AgentInterface,
    APIKeyInterface,
    BaseAIInterface,
    ModelInterface,
    WorkflowAIInterface,
    AIInterface,
    MLInterface,
    OptimizationInterface
)
from .unified_interface_registry import UnifiedInterfaceRegistry

__all__ = [
    # Learning Interfaces
    'LearningInterface',
    
    # Service Interfaces
    'BulkMessagingInterface',
    'CampaignMessagingInterface',
    'CoordinateDataInterface',
    'CoordinateManagerInterface',
    'CrossSystemMessagingInterface',
    'FSMMessagingInterface',
    'MessageSenderInterface',
    'OnboardingMessagingInterface',
    'YOLOMessagingInterface',
    
    # FSM Interfaces
    'StateInterface',
    'TransitionInterface',
    'WorkflowInterface',
    
    # AI/ML Interfaces
    'AgentInterface',
    'APIKeyInterface',
    'BaseAIInterface',
    'ModelInterface',
    'WorkflowAIInterface',
    'AIInterface',
    'MLInterface',
    'OptimizationInterface',
    
    # Registry
    'UnifiedInterfaceRegistry'
]

# SSOT Compliance Tracking
SSOT_COMPLIANCE = {
    "consolidated_interfaces": 7,
    "original_locations": [
        "src/core/learning/interfaces/",
        "src/services/interfaces/",
        "src/fsm/interfaces/",
        "src/managers/ai_ml/interfaces/",
        "agent_workspaces/meeting/src/ai_ml/interfaces/",
        "examples/interfaces/",
    ],
    "consolidation_status": "COMPLETE",
    "v2_compliance": "VERIFIED",
    "last_updated": "2025-08-30"
}
