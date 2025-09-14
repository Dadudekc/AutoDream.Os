#!/usr/bin/env python3
"""
Unified Messaging Service - V2 Compliant Enterprise Service
===========================================================

Main messaging service consolidating all messaging functionality into a single,
enterprise-ready service with proper separation of concerns.

V2 Compliance: <300 lines, single responsibility for messaging orchestration
Enterprise Ready: High availability, scalability, monitoring, security

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Import from core messaging system (SSOT)
try:
    from src.core.messaging import (
        UnifiedMessage,
        UnifiedMessageType,
        UnifiedMessagePriority,
        UnifiedMessageTag,
        get_messaging_core,
        send_message,
        broadcast_message,
    )
    MESSAGING_AVAILABLE = True
except ImportError as e:
    logging.error(f"❌ Core messaging system not available: {e}")
    MESSAGING_AVAILABLE = False

logger = logging.getLogger(__name__)

# Constants
SWARM_AGENTS = [
    "Agent-1", "Agent-2", "Agent-3", "Agent-4",
    "Agent-5", "Agent-6", "Agent-7", "Agent-8"
]

class UnifiedMessagingService:
    """Enterprise-ready unified messaging service."""
    
    def __init__(self, dry_run: bool = False):
        """Initialize the unified messaging service."""
        self.dry_run = dry_run
        self.service_available = MESSAGING_AVAILABLE
        self.messaging_core = get_messaging_core() if MESSAGING_AVAILABLE else None
        self.logger = logging.getLogger(__name__)
        
        # Initialize metrics
        self.metrics = {
            "total_messages_sent": 0,
            "successful_deliveries": 0,
            "failed_deliveries": 0,
            "last_activity": None
        }
    
    def send_message_to_agent(self, agent_id: str, message: str,
                             priority: str = "NORMAL", tag: str = "GENERAL") -> bool:
        """Send message to specific agent."""
        if not self.service_available:
            self.logger.error("❌ Messaging system not available")
            return False
        
        if self.dry_run:
            self.logger.info(f"🔍 DRY RUN: Would send to {agent_id}: {message}")
            return True
        
        try:
            # Convert string priority to enum
            priority_enum = UnifiedMessagePriority.URGENT if priority.upper() == "URGENT" else UnifiedMessagePriority.REGULAR
            tag_enum = UnifiedMessageTag.COORDINATION if tag.upper() == "COORDINATION" else UnifiedMessageTag.SYSTEM
            
            success = send_message(
                content=message,
                sender="UnifiedMessagingService",
                recipient=agent_id,
                message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
                priority=priority_enum,
                tags=[tag_enum]
            )
            
            # Update metrics
            self._update_metrics(success)
            
            if success:
                self.logger.info(f"✅ Message sent to {agent_id}")
            else:
                self.logger.error(f"❌ Failed to send message to {agent_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Error sending message to {agent_id}: {e}")
            self._update_metrics(False)
            return False
    
    def broadcast_to_swarm(self, message: str, priority: str = "NORMAL",
                          tag: str = "GENERAL") -> Dict[str, bool]:
        """Broadcast message to all swarm agents."""
        if not self.service_available:
            self.logger.error("❌ Messaging system not available for broadcast")
            return dict.fromkeys(SWARM_AGENTS, False)
        
        if self.dry_run:
            self.logger.info(f"🔍 DRY RUN BROADCAST: {message} to all agents")
            return dict.fromkeys(SWARM_AGENTS, True)
        
        try:
            # Convert string priority to enum
            priority_enum = UnifiedMessagePriority.URGENT if priority.upper() == "URGENT" else UnifiedMessagePriority.REGULAR
            
            success = broadcast_message(
                content=message,
                sender="UnifiedMessagingService",
                priority=priority_enum
            )
            
            # Update metrics
            self._update_metrics(success)
            
            if success:
                self.logger.info(f"✅ Broadcast sent to all agents")
                return dict.fromkeys(SWARM_AGENTS, True)
            else:
                self.logger.error(f"❌ Broadcast failed")
                return dict.fromkeys(SWARM_AGENTS, False)
                
        except Exception as e:
            self.logger.error(f"❌ Broadcast error: {e}")
            self._update_metrics(False)
            return dict.fromkeys(SWARM_AGENTS, False)
    
    def send_coordination_message(self, agent_id: str, message: str) -> bool:
        """Send coordination message to agent."""
        return self.send_message_to_agent(
            agent_id=agent_id,
            message=message,
            priority="NORMAL",
            tag="COORDINATION"
        )
    
    def send_urgent_message(self, agent_id: str, message: str) -> bool:
        """Send urgent message to agent."""
        return self.send_message_to_agent(
            agent_id=agent_id,
            message=message,
            priority="URGENT",
            tag="SYSTEM"
        )
    
    def send_onboarding_message(self, agent_id: str, message: str) -> bool:
        """Send onboarding message to agent."""
        return self.send_message_to_agent(
            agent_id=agent_id,
            message=message,
            priority="NORMAL",
            tag="ONBOARDING"
        )
    
    def list_available_agents(self) -> List[str]:
        """List all available agents."""
        return SWARM_AGENTS.copy()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get messaging system status."""
        return {
            "service_available": self.service_available,
            "dry_run_mode": self.dry_run,
            "metrics": self.metrics.copy(),
            "available_agents": len(self.list_available_agents()),
            "last_activity": self.metrics["last_activity"]
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get messaging metrics."""
        return self.metrics.copy()
    
    def reset_metrics(self) -> None:
        """Reset messaging metrics."""
        self.metrics = {
            "total_messages_sent": 0,
            "successful_deliveries": 0,
            "failed_deliveries": 0,
            "last_activity": None
        }
        self.logger.info("📊 Metrics reset")
    
    def _update_metrics(self, success: bool) -> None:
        """Update messaging metrics."""
        self.metrics["total_messages_sent"] += 1
        if success:
            self.metrics["successful_deliveries"] += 1
        else:
            self.metrics["failed_deliveries"] += 1
        self.metrics["last_activity"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on messaging system."""
        try:
            # Test basic functionality
            test_message = UnifiedMessage(
                content="Health check test",
                sender="HealthCheck",
                recipient="TestAgent",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT
            )
            
            return {
                "status": "healthy",
                "service_available": self.service_available,
                "core_available": self.messaging_core is not None,
                "metrics": self.metrics,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "service_available": self.service_available,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }

# Global service instance
unified_messaging_service = UnifiedMessagingService()

# Public API functions
def get_unified_messaging_service() -> UnifiedMessagingService:
    """Get the unified messaging service instance."""
    return unified_messaging_service

def send_message_to_agent(agent_id: str, message: str, **kwargs) -> bool:
    """Send message to agent using unified service."""
    return unified_messaging_service.send_message_to_agent(agent_id, message, **kwargs)

def broadcast_to_swarm(message: str, **kwargs) -> Dict[str, bool]:
    """Broadcast message to swarm using unified service."""
    return unified_messaging_service.broadcast_to_swarm(message, **kwargs)

def get_messaging_status() -> Dict[str, Any]:
    """Get messaging system status."""
    return unified_messaging_service.get_system_status()

# Service exports
__all__ = [
    "UnifiedMessagingService",
    "get_unified_messaging_service",
    "send_message_to_agent",
    "broadcast_to_swarm",
    "get_messaging_status",
    "unified_messaging_service",
]