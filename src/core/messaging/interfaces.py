#!/usr/bin/env python3
"""
Messaging Interfaces - V2 Compliant Protocol Definitions
=======================================================

Protocol definitions for the unified messaging system.
Defines interfaces for message delivery, onboarding, and coordination.

V2 Compliance: <300 lines, single responsibility for interface definitions
Enterprise Ready: Type-safe protocols, comprehensive interface coverage

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, Tuple
from datetime import datetime

from .models import (
    UnifiedMessage,
    AgentCoordinates,
    MessageHistory,
    MessagingMetrics,
    DeliveryMethod,
    MessageStatus
)

# ============================================================================
# CORE MESSAGING INTERFACES
# ============================================================================

class IMessageDelivery(Protocol):
    """Interface for message delivery mechanisms."""
    
    def send_message(self, message: UnifiedMessage) -> bool:
        """Send a message using this delivery mechanism."""
        ...
    
    def can_deliver(self, message: UnifiedMessage) -> bool:
        """Check if this delivery mechanism can handle the message."""
        ...
    
    def get_delivery_method(self) -> DeliveryMethod:
        """Get the delivery method this interface implements."""
        ...

class IOnboardingService(Protocol):
    """Interface for agent onboarding services."""
    
    def onboard_agent(self, agent_id: str, message: str) -> bool:
        """Onboard a single agent."""
        ...
    
    def onboard_swarm(self, message: str) -> Dict[str, bool]:
        """Onboard all agents in the swarm."""
        ...
    
    def get_onboarding_status(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get onboarding status for agent or all agents."""
        ...

class ICoordinateProvider(Protocol):
    """Interface for coordinate providers."""
    
    def get_agent_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get coordinates for a specific agent."""
        ...
    
    def get_all_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """Get coordinates for all agents."""
        ...
    
    def is_agent_active(self, agent_id: str) -> bool:
        """Check if an agent is active."""
        ...

class IMessageHistory(Protocol):
    """Interface for message history management."""
    
    def add_message(self, message: UnifiedMessage) -> None:
        """Add a message to history."""
        ...
    
    def get_message_history(self, agent_id: Optional[str] = None, 
                          limit: int = 100) -> List[MessageHistory]:
        """Get message history for agent or all agents."""
        ...
    
    def update_message_status(self, message_id: str, status: MessageStatus) -> None:
        """Update message status in history."""
        ...

class IMessagingMetrics(Protocol):
    """Interface for messaging metrics collection."""
    
    def record_message_sent(self, message: UnifiedMessage, success: bool) -> None:
        """Record a message send attempt."""
        ...
    
    def get_metrics(self) -> MessagingMetrics:
        """Get current messaging metrics."""
        ...
    
    def reset_metrics(self) -> None:
        """Reset messaging metrics."""
        ...

# ============================================================================
# ABSTRACT BASE CLASSES
# ============================================================================

class BaseMessageDelivery(ABC):
    """Abstract base class for message delivery implementations."""
    
    def __init__(self, delivery_method: DeliveryMethod):
        self.delivery_method = delivery_method
        self.metrics: Optional[IMessagingMetrics] = None
    
    @abstractmethod
    def send_message(self, message: UnifiedMessage) -> bool:
        """Send a message using this delivery mechanism."""
        pass
    
    @abstractmethod
    def can_deliver(self, message: UnifiedMessage) -> bool:
        """Check if this delivery mechanism can handle the message."""
        pass
    
    def get_delivery_method(self) -> DeliveryMethod:
        """Get the delivery method this class implements."""
        return self.delivery_method
    
    def set_metrics(self, metrics: IMessagingMetrics) -> None:
        """Set metrics collector for this delivery mechanism."""
        self.metrics = metrics
    
    def _record_metrics(self, message: UnifiedMessage, success: bool) -> None:
        """Record metrics for message delivery."""
        if self.metrics:
            self.metrics.record_message_sent(message, success)

class BaseOnboardingService(ABC):
    """Abstract base class for onboarding service implementations."""
    
    def __init__(self):
        self.messaging_service: Optional[IMessageDelivery] = None
    
    @abstractmethod
    def onboard_agent(self, agent_id: str, message: str) -> bool:
        """Onboard a single agent."""
        pass
    
    @abstractmethod
    def onboard_swarm(self, message: str) -> Dict[str, bool]:
        """Onboard all agents in the swarm."""
        pass
    
    @abstractmethod
    def get_onboarding_status(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get onboarding status for agent or all agents."""
        pass
    
    def set_messaging_service(self, messaging_service: IMessageDelivery) -> None:
        """Set the messaging service for onboarding."""
        self.messaging_service = messaging_service

class BaseCoordinateProvider(ABC):
    """Abstract base class for coordinate provider implementations."""
    
    @abstractmethod
    def get_agent_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get coordinates for a specific agent."""
        pass
    
    @abstractmethod
    def get_all_coordinates(self) -> Dict[str, Tuple[int, int]]:
        """Get coordinates for all agents."""
        pass
    
    @abstractmethod
    def is_agent_active(self, agent_id: str) -> bool:
        """Check if an agent is active."""
        pass

# ============================================================================
# UTILITY INTERFACES
# ============================================================================

class IMessageValidator(Protocol):
    """Interface for message validation."""
    
    def validate_message(self, message: UnifiedMessage) -> Tuple[bool, Optional[str]]:
        """Validate a message. Returns (is_valid, error_message)."""
        ...

class IMessageFormatter(Protocol):
    """Interface for message formatting."""
    
    def format_message(self, message: UnifiedMessage) -> str:
        """Format a message for delivery."""
        ...

class IMessageRouter(Protocol):
    """Interface for message routing."""
    
    def route_message(self, message: UnifiedMessage) -> IMessageDelivery:
        """Route a message to the appropriate delivery mechanism."""
        ...

class IRetryHandler(Protocol):
    """Interface for retry handling."""
    
    def should_retry(self, message: UnifiedMessage, attempt: int) -> bool:
        """Determine if a message should be retried."""
        ...
    
    def get_retry_delay(self, message: UnifiedMessage, attempt: int) -> float:
        """Get the delay before retrying a message."""
        ...

# ============================================================================
# FACTORY INTERFACES
# ============================================================================

class IMessageDeliveryFactory(Protocol):
    """Interface for message delivery factory."""
    
    def create_delivery(self, delivery_method: DeliveryMethod) -> IMessageDelivery:
        """Create a message delivery instance."""
        ...

class IOnboardingServiceFactory(Protocol):
    """Interface for onboarding service factory."""
    
    def create_onboarding_service(self) -> IOnboardingService:
        """Create an onboarding service instance."""
        ...

# ============================================================================
# CONFIGURATION INTERFACES
# ============================================================================

class IMessagingConfig(Protocol):
    """Interface for messaging configuration."""
    
    def get_delivery_method(self, message: UnifiedMessage) -> DeliveryMethod:
        """Get the preferred delivery method for a message."""
        ...
    
    def get_retry_config(self) -> Dict[str, Any]:
        """Get retry configuration."""
        ...
    
    def get_coordinate_config(self) -> Dict[str, Any]:
        """Get coordinate configuration."""
        ...

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Core Interfaces
    "IMessageDelivery",
    "IOnboardingService", 
    "ICoordinateProvider",
    "IMessageHistory",
    "IMessagingMetrics",
    
    # Abstract Base Classes
    "BaseMessageDelivery",
    "BaseOnboardingService",
    "BaseCoordinateProvider",
    
    # Utility Interfaces
    "IMessageValidator",
    "IMessageFormatter",
    "IMessageRouter",
    "IRetryHandler",
    
    # Factory Interfaces
    "IMessageDeliveryFactory",
    "IOnboardingServiceFactory",
    
    # Configuration Interfaces
    "IMessagingConfig",
]