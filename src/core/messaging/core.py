#!/usr/bin/env python3
"""
Messaging Core - V2 Compliant Unified Messaging System
=====================================================

SINGLE SOURCE OF TRUTH for all messaging functionality.
Consolidated from src/core/messaging_core.py with improved architecture.

V2 Compliance: <300 lines, single responsibility for core messaging
Enterprise Ready: High availability, scalability, monitoring, error handling

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    DeliveryMethod,
    MessageStatus,
    create_message,
    create_broadcast_message,
    create_onboarding_message
)
from .interfaces import (
    IMessageDelivery,
    IOnboardingService,
    IMessageHistory,
    IMessagingMetrics,
    BaseMessageDelivery
)

logger = logging.getLogger(__name__)

class UnifiedMessagingCore:
    """SINGLE SOURCE OF TRUTH for all messaging functionality."""

    def __init__(self, delivery_service: Optional[IMessageDelivery] = None,
                 onboarding_service: Optional[IOnboardingService] = None,
                 message_history: Optional[IMessageHistory] = None,
                 metrics: Optional[IMessagingMetrics] = None):
        """Initialize the unified messaging core."""
        self.delivery_service = delivery_service
        self.onboarding_service = onboarding_service
        self.message_history = message_history
        self.metrics = metrics
        self.logger = logging.getLogger(__name__)

        # Initialize subsystems
        self._initialize_subsystems()

    def _initialize_subsystems(self):
        """Initialize all messaging subsystems."""
        # Import and initialize delivery services
        try:
            from .delivery.pyautogui import PyAutoGUIMessagingDelivery
            if not self.delivery_service:
                self.delivery_service = PyAutoGUIMessagingDelivery()
        except ImportError:
            self.logger.warning("PyAutoGUI delivery service not available")

        # Import and initialize onboarding service
        try:
            from .onboarding_service import OnboardingService
            if not self.onboarding_service:
                self.onboarding_service = OnboardingService()
        except ImportError:
            self.logger.warning("Onboarding service not available")

    def send_message(self, content: str, sender: str, recipient: str,
                    message_type: UnifiedMessageType,
                    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                    tags: Optional[List[UnifiedMessageTag]] = None,
                    metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Send a message using the unified messaging system."""
        message = create_message(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags,
            metadata=metadata
        )

        return self.send_message_object(message)

    def send_message_object(self, message: UnifiedMessage) -> bool:
        """Send a UnifiedMessage object."""
        try:
            # Update message status
            message.status = MessageStatus.PENDING
            
            # Record in history
            if self.message_history:
                self.message_history.add_message(message)

            # Send via delivery service
            if self.delivery_service:
                success = self.delivery_service.send_message(message)
                
                # Update status based on result
                message.status = MessageStatus.SENT if success else MessageStatus.FAILED
                
                # Record metrics
                if self.metrics:
                    self.metrics.record_message_sent(message, success)
                
                return success
            else:
                self.logger.error("No delivery service configured")
                message.status = MessageStatus.FAILED
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            message.status = MessageStatus.FAILED
            if self.metrics:
                self.metrics.record_message_sent(message, False)
            return False

    def send_message_to_inbox(self, message: UnifiedMessage, max_retries: int = 3) -> bool:
        """Send message to agent inbox with retry logic."""
        try:
            # Create inbox file path in agent workspace
            inbox_dir = Path("agent_workspaces") / message.recipient / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create timestamped filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"CAPTAIN_MESSAGE_{timestamp}_{message.message_id[:8]}.md"
            filepath = inbox_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                # Write message in markdown format
                f.write(f'# 🚨 CAPTAIN MESSAGE - {message.message_type.value.upper()}\n\n')
                f.write(f'**From**: {message.sender}\n')
                f.write(f'**To**: {message.recipient}\n')
                f.write(f'**Priority**: {message.priority.value}\n')
                f.write(f'**Message ID**: {message.message_id}\n')
                f.write(f'**Timestamp**: {message.timestamp.isoformat()}\n')
                if message.tags:
                    f.write(f'**Tags**: {", ".join(tag.value for tag in message.tags)}\n')
                f.write('\n---\n\n')
                f.write(f'{message.content}\n')
                f.write('\n---\n')
                f.write('*Message delivered via Unified Messaging Service*\n')

            self.logger.info(f"Message sent to inbox: {message.recipient}")
            message.status = MessageStatus.DELIVERED
            return True

        except Exception as e:
            self.logger.error(f"Failed to send message to inbox: {e}")
            message.status = MessageStatus.FAILED
            return False

    def broadcast_message(self, content: str, sender: str = "Captain Agent-4", 
                         priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR) -> bool:
        """Broadcast message to all agents."""
        message = create_broadcast_message(content, sender, priority)
        return self.send_message_object(message)

    def generate_onboarding_message(self, agent_id: str, style: str = "standard") -> str:
        """Generate onboarding message for an agent."""
        if self.onboarding_service:
            return self.onboarding_service.generate_onboarding_message(agent_id, style)
        else:
            return f"Welcome {agent_id}! You have been onboarded to the V2_SWARM system."

    def onboard_agent(self, agent_id: str, style: str = "standard") -> bool:
        """Onboard a single agent."""
        if self.onboarding_service:
            message = self.generate_onboarding_message(agent_id, style)
            return self.onboarding_service.onboard_agent(agent_id, message)
        else:
            # Fallback onboarding
            message = create_onboarding_message(
                content=f"Welcome {agent_id}! You are now part of the V2_SWARM.",
                agent_id=agent_id
            )
            return self.send_message_object(message)

    def onboard_swarm(self, style: str = "standard") -> Dict[str, bool]:
        """Onboard all agents in the swarm."""
        if self.onboarding_service:
            return self.onboarding_service.onboard_swarm(style)
        else:
            # Fallback swarm onboarding
            agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", 
                     "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
            results = {}
            for agent_id in agents:
                results[agent_id] = self.onboard_agent(agent_id, style)
            return results

    def list_agents(self) -> List[str]:
        """List all available agents."""
        return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", 
                "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

    def get_system_status(self) -> Dict[str, Any]:
        """Get messaging system status."""
        return {
            "delivery_service_available": self.delivery_service is not None,
            "onboarding_service_available": self.onboarding_service is not None,
            "message_history_available": self.message_history is not None,
            "metrics_available": self.metrics is not None,
            "available_agents": len(self.list_agents()),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on messaging system."""
        try:
            # Test basic functionality
            test_message = create_message(
                content="Health check test",
                sender="HealthCheck",
                recipient="TestAgent",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT
            )
            
            return {
                "status": "healthy",
                "delivery_service": self.delivery_service is not None,
                "onboarding_service": self.onboarding_service is not None,
                "message_history": self.message_history is not None,
                "metrics": self.metrics is not None,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

# SINGLE GLOBAL INSTANCE - THE ONE TRUE MESSAGING CORE
messaging_core = UnifiedMessagingCore()

# PUBLIC API - Single point of access for all messaging
def get_messaging_core() -> UnifiedMessagingCore:
    """Get the SINGLE SOURCE OF TRUTH messaging core."""
    return messaging_core

def send_message(content: str, sender: str, recipient: str,
                message_type: UnifiedMessageType,
                priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                tags: Optional[List[UnifiedMessageTag]] = None,
                metadata: Optional[Dict[str, Any]] = None) -> bool:
    """Send message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.send_message(content, sender, recipient, message_type, priority, tags, metadata)

def send_message_object(message: UnifiedMessage) -> bool:
    """Send UnifiedMessage using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.send_message_object(message)

def broadcast_message(content: str, sender: str = "Captain Agent-4", 
                     priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR) -> bool:
    """Broadcast message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.broadcast_message(content, sender, priority)

def generate_onboarding_message(agent_id: str, style: str = "standard") -> str:
    """Generate onboarding message using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.generate_onboarding_message(agent_id, style)

def onboard_agent(agent_id: str, style: str = "standard") -> bool:
    """Onboard agent using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.onboard_agent(agent_id, style)

def onboard_swarm(style: str = "standard") -> Dict[str, bool]:
    """Onboard swarm using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.onboard_swarm(style)

def list_agents() -> List[str]:
    """List agents using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.list_agents()

def get_system_status() -> Dict[str, Any]:
    """Get system status using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.get_system_status()

def health_check() -> Dict[str, Any]:
    """Perform health check using the SINGLE SOURCE OF TRUTH."""
    return messaging_core.health_check()

# EXPORTS
__all__ = [
    # Core class
    "UnifiedMessagingCore",
    
    # Public API functions
    "get_messaging_core",
    "send_message",
    "send_message_object", 
    "broadcast_message",
    "generate_onboarding_message",
    "onboard_agent",
    "onboard_swarm",
    "list_agents",
    "get_system_status",
    "health_check",
    
    # Global instance
    "messaging_core",
]