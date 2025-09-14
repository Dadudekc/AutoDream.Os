#!/usr/bin/env python3
"""
Broadcast Service - V2 Compliant Mass Communication
==================================================

Service for managing mass communication and broadcast operations across the swarm.

V2 Compliance: <300 lines, single responsibility for broadcast operations
Enterprise Ready: High availability, scalability, monitoring, error handling

Author: Agent-4 (Captain) - V2_SWARM Consolidation
License: MIT
"""

import logging
import time
from typing import Dict, List, Optional, Any, Union
from enum import Enum

try:
    from src.services.messaging.unified_service import get_unified_messaging_service
    MESSAGING_AVAILABLE = True
except ImportError as e:
    logging.error(f"❌ Messaging service not available: {e}")
    MESSAGING_AVAILABLE = False

logger = logging.getLogger(__name__)

class BroadcastType(Enum):
    """Broadcast type options."""
    GENERAL = "general"
    COORDINATION = "coordination"
    EMERGENCY = "emergency"
    STATUS_UPDATE = "status_update"
    TASK_ASSIGNMENT = "task_assignment"
    SYSTEM_ALERT = "system_alert"

class BroadcastPriority(Enum):
    """Broadcast priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class BroadcastService:
    """V2 compliant broadcast service for mass communication."""
    
    def __init__(self):
        """Initialize the broadcast service."""
        self.messaging_service = get_unified_messaging_service() if MESSAGING_AVAILABLE else None
        self.logger = logging.getLogger(__name__)
        
        # Broadcast tracking
        self.broadcast_history = []
        self.broadcast_metrics = {
            "total_broadcasts": 0,
            "successful_broadcasts": 0,
            "failed_broadcasts": 0,
            "last_broadcast": None
        }
        
        # Agent list
        self.swarm_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
    
    def broadcast_message(self, message: str, broadcast_type: BroadcastType = BroadcastType.GENERAL,
                         priority: BroadcastPriority = BroadcastPriority.NORMAL,
                         target_agents: Optional[List[str]] = None) -> Dict[str, bool]:
        """Broadcast message to specified agents or all agents."""
        if not self.messaging_service:
            self.logger.error("❌ Messaging service not available")
            return dict.fromkeys(self.swarm_agents, False)
        
        try:
            # Determine target agents
            agents = target_agents or self.swarm_agents
            
            # Format message based on type
            formatted_message = self._format_broadcast_message(message, broadcast_type, priority)
            
            # Send broadcast
            results = self.messaging_service.broadcast_to_swarm(
                message=formatted_message,
                priority=priority.value.upper(),
                tag=broadcast_type.value.upper()
            )
            
            # Track broadcast
            self._track_broadcast(broadcast_type, priority, message, results)
            
            # Update metrics
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            
            if successful > 0:
                self.logger.info(f"✅ Broadcast sent to {successful}/{total} agents")
            else:
                self.logger.error(f"❌ Broadcast failed to all agents")
            
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Broadcast error: {e}")
            self._track_broadcast(broadcast_type, priority, message, {}, error=str(e))
            return dict.fromkeys(agents, False)
    
    def broadcast_coordination_message(self, message: str, priority: BroadcastPriority = BroadcastPriority.NORMAL) -> Dict[str, bool]:
        """Broadcast coordination message to all agents."""
        return self.broadcast_message(
            message=message,
            broadcast_type=BroadcastType.COORDINATION,
            priority=priority
        )
    
    def broadcast_emergency_alert(self, message: str) -> Dict[str, bool]:
        """Broadcast emergency alert to all agents."""
        return self.broadcast_message(
            message=message,
            broadcast_type=BroadcastType.EMERGENCY,
            priority=BroadcastPriority.URGENT
        )
    
    def broadcast_status_update(self, message: str) -> Dict[str, bool]:
        """Broadcast status update to all agents."""
        return self.broadcast_message(
            message=message,
            broadcast_type=BroadcastType.STATUS_UPDATE,
            priority=BroadcastPriority.NORMAL
        )
    
    def broadcast_task_assignment(self, message: str, priority: BroadcastPriority = BroadcastPriority.NORMAL) -> Dict[str, bool]:
        """Broadcast task assignment to all agents."""
        return self.broadcast_message(
            message=message,
            broadcast_type=BroadcastType.TASK_ASSIGNMENT,
            priority=priority
        )
    
    def broadcast_system_alert(self, message: str, priority: BroadcastPriority = BroadcastPriority.HIGH) -> Dict[str, bool]:
        """Broadcast system alert to all agents."""
        return self.broadcast_message(
            message=message,
            broadcast_type=BroadcastType.SYSTEM_ALERT,
            priority=priority
        )
    
    def broadcast_to_subset(self, message: str, agent_ids: List[str],
                           broadcast_type: BroadcastType = BroadcastType.GENERAL,
                           priority: BroadcastPriority = BroadcastPriority.NORMAL) -> Dict[str, bool]:
        """Broadcast message to specific subset of agents."""
        return self.broadcast_message(
            message=message,
            broadcast_type=broadcast_type,
            priority=priority,
            target_agents=agent_ids
        )
    
    def get_broadcast_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get broadcast history."""
        return self.broadcast_history[-limit:] if limit > 0 else self.broadcast_history.copy()
    
    def get_broadcast_metrics(self) -> Dict[str, Any]:
        """Get broadcast metrics."""
        return self.broadcast_metrics.copy()
    
    def reset_broadcast_metrics(self) -> None:
        """Reset broadcast metrics."""
        self.broadcast_metrics = {
            "total_broadcasts": 0,
            "successful_broadcasts": 0,
            "failed_broadcasts": 0,
            "last_broadcast": None
        }
        self.logger.info("📊 Broadcast metrics reset")
    
    def _format_broadcast_message(self, message: str, broadcast_type: BroadcastType, priority: BroadcastPriority) -> str:
        """Format broadcast message based on type and priority."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if broadcast_type == BroadcastType.EMERGENCY:
            return f"""🚨 EMERGENCY BROADCAST

**From:** Captain Agent-4
**To:** ALL AGENTS
**Priority:** URGENT
**Timestamp:** {timestamp}

**EMERGENCY MESSAGE:**
{message}

**IMMEDIATE ACTION REQUIRED:**
• Acknowledge receipt immediately
• Follow emergency protocols
• Report status to Captain
• Stand by for further instructions

🚨 EMERGENCY PROTOCOL ACTIVATED - ALL AGENTS RESPOND! 🚨"""
        
        elif broadcast_type == BroadcastType.COORDINATION:
            return f"""🎯 COORDINATION BROADCAST

**From:** Captain Agent-4
**To:** ALL AGENTS
**Priority:** {priority.value.upper()}
**Timestamp:** {timestamp}

**Coordination Message:**
{message}

**Coordination Protocol:**
• Acknowledge receipt
• Update status files
• Follow coordination instructions
• Report completion

🐝 WE ARE SWARM - Coordination message delivered! ⚡️"""
        
        elif broadcast_type == BroadcastType.TASK_ASSIGNMENT:
            return f"""📋 TASK ASSIGNMENT BROADCAST

**From:** Captain Agent-4
**To:** ALL AGENTS
**Priority:** {priority.value.upper()}
**Timestamp:** {timestamp}

**Task Assignment:**
{message}

**Assignment Protocol:**
• Acknowledge receipt
• Review task requirements
• Update status files
• Begin task execution
• Report progress regularly

🐝 WE ARE SWARM - Task assignment delivered! ⚡️"""
        
        elif broadcast_type == BroadcastType.SYSTEM_ALERT:
            return f"""⚠️ SYSTEM ALERT BROADCAST

**From:** Captain Agent-4
**To:** ALL AGENTS
**Priority:** {priority.value.upper()}
**Timestamp:** {timestamp}

**System Alert:**
{message}

**Alert Protocol:**
• Acknowledge receipt
• Review system status
• Update status files
• Follow alert procedures
• Report any issues

🐝 WE ARE SWARM - System alert delivered! ⚡️"""
        
        else:  # GENERAL or STATUS_UPDATE
            return f"""📢 SWARM BROADCAST

**From:** Captain Agent-4
**To:** ALL AGENTS
**Priority:** {priority.value.upper()}
**Timestamp:** {timestamp}

**Message:**
{message}

**Coordination Protocol:**
• Acknowledge receipt
• Update status files
• Follow instructions provided
• Report completion

🐝 WE ARE SWARM - Broadcast message delivered! ⚡️"""
    
    def _track_broadcast(self, broadcast_type: BroadcastType, priority: BroadcastPriority,
                        message: str, results: Dict[str, bool], error: Optional[str] = None) -> None:
        """Track broadcast activity."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate success metrics
        successful = sum(1 for success in results.values() if success)
        total = len(results) if results else 0
        
        # Update metrics
        self.broadcast_metrics["total_broadcasts"] += 1
        if successful > 0:
            self.broadcast_metrics["successful_broadcasts"] += 1
        else:
            self.broadcast_metrics["failed_broadcasts"] += 1
        self.broadcast_metrics["last_broadcast"] = timestamp
        
        # Add to history
        self.broadcast_history.append({
            "timestamp": timestamp,
            "broadcast_type": broadcast_type.value,
            "priority": priority.value,
            "message": message[:100] + "..." if len(message) > 100 else message,
            "target_agents": list(results.keys()) if results else [],
            "successful": successful,
            "total": total,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "error": error
        })
        
        # Keep only last 100 entries
        if len(self.broadcast_history) > 100:
            self.broadcast_history = self.broadcast_history[-100:]

# Global service instance
broadcast_service = BroadcastService()

# Public API functions
def get_broadcast_service() -> BroadcastService:
    """Get the broadcast service instance."""
    return broadcast_service

def broadcast_message(message: str, broadcast_type: BroadcastType = BroadcastType.GENERAL,
                     priority: BroadcastPriority = BroadcastPriority.NORMAL,
                     target_agents: Optional[List[str]] = None) -> Dict[str, bool]:
    """Broadcast message using broadcast service."""
    return broadcast_service.broadcast_message(message, broadcast_type, priority, target_agents)

def broadcast_emergency_alert(message: str) -> Dict[str, bool]:
    """Broadcast emergency alert."""
    return broadcast_service.broadcast_emergency_alert(message)

def broadcast_coordination_message(message: str, priority: BroadcastPriority = BroadcastPriority.NORMAL) -> Dict[str, bool]:
    """Broadcast coordination message."""
    return broadcast_service.broadcast_coordination_message(message, priority)

# Service exports
__all__ = [
    "BroadcastService",
    "BroadcastType",
    "BroadcastPriority",
    "get_broadcast_service",
    "broadcast_message",
    "broadcast_emergency_alert",
    "broadcast_coordination_message",
    "broadcast_service",
]