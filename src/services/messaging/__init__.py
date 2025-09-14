"""
Unified Messaging Service Layer - V2 Compliant Enterprise Services
================================================================

Consolidated service layer providing enterprise-ready messaging functionality.

V2 Compliance: <300 lines per module, single responsibility
Enterprise Ready: High availability, scalability, monitoring, security

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

# Core messaging services
from .unified_service import (
    UnifiedMessagingService,
    get_unified_messaging_service,
    send_message_to_agent,
    broadcast_to_swarm,
    get_messaging_status,
    unified_messaging_service,
)

# CLI services
from .cli.messaging_cli import (
    UnifiedMessagingCLI,
)

# Onboarding services
from .onboarding.onboarding_service import (
    OnboardingService,
    get_onboarding_service,
    onboard_agent,
    onboard_swarm,
    onboarding_service,
)

from .onboarding.message_generator import (
    OnboardingMessageGenerator,
    MessageStyle,
    MessageType,
    get_message_generator,
    generate_onboarding_message,
    generate_coordination_message,
    message_generator,
)

# Broadcast services
from .broadcast.broadcast_service import (
    BroadcastService,
    BroadcastType,
    BroadcastPriority,
    get_broadcast_service,
    broadcast_message,
    broadcast_emergency_alert,
    broadcast_coordination_message,
    broadcast_service,
)

from .broadcast.coordination_service import (
    CoordinationService,
    CoordinationStatus,
    TaskPriority,
    CoordinationTask,
    get_coordination_service,
    assign_task,
    complete_task,
    request_status_updates,
    coordination_service,
)

# Service exports
__all__ = [
    # Core services
    "UnifiedMessagingService",
    "get_unified_messaging_service",
    "send_message_to_agent",
    "broadcast_to_swarm",
    "get_messaging_status",
    "unified_messaging_service",
    
    # CLI services
    "UnifiedMessagingCLI",
    
    # Onboarding services
    "OnboardingService",
    "get_onboarding_service",
    "onboard_agent",
    "onboard_swarm",
    "onboarding_service",
    
    "OnboardingMessageGenerator",
    "MessageStyle",
    "MessageType",
    "get_message_generator",
    "generate_onboarding_message",
    "generate_coordination_message",
    "message_generator",
    
    # Broadcast services
    "BroadcastService",
    "BroadcastType",
    "BroadcastPriority",
    "get_broadcast_service",
    "broadcast_message",
    "broadcast_emergency_alert",
    "broadcast_coordination_message",
    "broadcast_service",
    
    "CoordinationService",
    "CoordinationStatus",
    "TaskPriority",
    "CoordinationTask",
    "get_coordination_service",
    "assign_task",
    "complete_task",
    "request_status_updates",
    "coordination_service",
]

# Version info
__version__ = "2.0.0"
__author__ = "Agent-4 (Captain) - V2_SWARM"
__license__ = "MIT"