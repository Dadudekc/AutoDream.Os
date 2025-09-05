#!/usr/bin/env python3
"""
Messaging Coordination Handler - V2 Compliance Module
===================================================

Message coordination and routing system for the messaging service.

V2 Compliance: < 300 lines, single responsibility, coordination management.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
from typing import Any, Dict, List, Optional
from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
    RecipientType
)


class MessagingCoordinationHandler:
    """
    Message coordination and routing system.
    
    Provides comprehensive coordination capabilities while maintaining
    all original functionality through efficient design.
    """
    
    def __init__(self):
        """Initialize coordination handler."""
        self.coordination_rules = self._initialize_coordination_rules()
        self.routing_table = self._initialize_routing_table()
        self.coordination_stats = {
            "total_coordinations": 0,
            "successful_coordinations": 0,
            "failed_coordinations": 0,
            "average_coordination_time": 0.0
        }
    
    def _initialize_coordination_rules(self) -> Dict[str, Any]:
        """Initialize coordination rules."""
        return {
            "priority_routing": {
                UnifiedMessagePriority.URGENT: "immediate",
                UnifiedMessagePriority.REGULAR: "standard"
            },
            "type_routing": {
                UnifiedMessageType.ONBOARDING: "system_priority",
                UnifiedMessageType.BROADCAST: "all_agents",
                UnifiedMessageType.A2A: "agent_to_agent",
                UnifiedMessageType.S2A: "system_to_agent",
                UnifiedMessageType.H2A: "human_to_agent",
                UnifiedMessageType.C2A: "captain_priority"
            },
            "sender_routing": {
                SenderType.CAPTAIN: "highest_priority",
                SenderType.SYSTEM: "high_priority",
                SenderType.AGENT: "standard_priority",
                SenderType.HUMAN: "standard_priority"
            }
        }
    
    def _initialize_routing_table(self) -> Dict[str, str]:
        """Initialize message routing table."""
        return {
            "Agent-1": "standard_delivery",
            "Agent-2": "standard_delivery",
            "Agent-3": "standard_delivery",
            "Agent-4": "captain_delivery",
            "Agent-5": "standard_delivery",
            "Agent-6": "standard_delivery",
            "Agent-7": "standard_delivery",
            "Agent-8": "standard_delivery",
            "All Agents": "broadcast_delivery",
            "System": "system_delivery"
        }
    
    def coordinate_message(self, message: UnifiedMessage) -> Dict[str, Any]:
        """
        Coordinate message delivery based on message properties.
        
        Args:
            message: Message to coordinate
            
        Returns:
            Coordination result dictionary
        """
        start_time = time.time()
        
        try:
            # Determine coordination strategy
            strategy = self._determine_coordination_strategy(message)
            
            # Apply coordination rules
            coordination_result = self._apply_coordination_rules(message, strategy)
            
            # Update statistics
            self._update_coordination_stats(True, time.time() - start_time)
            
            return {
                "success": True,
                "strategy": strategy,
                "coordination_result": coordination_result,
                "message_id": message.message_id,
                "recipient": message.recipient
            }
            
        except Exception as e:
            self._update_coordination_stats(False, time.time() - start_time)
            return {
                "success": False,
                "error": str(e),
                "message_id": message.message_id
            }
    
    def coordinate_bulk_messages(self, messages: List[UnifiedMessage]) -> Dict[str, Any]:
        """
        Coordinate multiple messages for efficient delivery.
        
        Args:
            messages: List of messages to coordinate
            
        Returns:
            Bulk coordination result dictionary
        """
        start_time = time.time()
        results = []
        successful = 0
        failed = 0
        
        # Group messages by coordination strategy
        grouped_messages = self._group_messages_by_strategy(messages)
        
        for strategy, message_group in grouped_messages.items():
            for message in message_group:
                result = self.coordinate_message(message)
                results.append(result)
                
                if result["success"]:
                    successful += 1
                else:
                    failed += 1
        
        execution_time = time.time() - start_time
        
        return {
            "success": True,
            "total_messages": len(messages),
            "successful": successful,
            "failed": failed,
            "execution_time": execution_time,
            "results": results,
            "grouped_by_strategy": len(grouped_messages)
        }
    
    def _determine_coordination_strategy(self, message: UnifiedMessage) -> str:
        """Determine the best coordination strategy for a message."""
        # Check priority-based routing
        priority_strategy = self.coordination_rules["priority_routing"].get(
            message.priority, "standard"
        )
        
        # Check type-based routing
        type_strategy = self.coordination_rules["type_routing"].get(
            message.message_type, "standard"
        )
        
        # Check sender-based routing
        sender_strategy = self.coordination_rules["sender_routing"].get(
            message.sender_type, "standard"
        )
        
        # Determine final strategy based on precedence
        if sender_strategy == "highest_priority":
            return "captain_priority"
        elif priority_strategy == "immediate":
            return "urgent_delivery"
        elif type_strategy == "system_priority":
            return "system_priority"
        elif type_strategy == "broadcast":
            return "broadcast_delivery"
        else:
            return "standard_delivery"
    
    def _apply_coordination_rules(self, message: UnifiedMessage, strategy: str) -> Dict[str, Any]:
        """Apply coordination rules based on strategy."""
        rules_applied = []
        
        # Apply priority rules
        if message.priority == UnifiedMessagePriority.URGENT:
            rules_applied.append("urgent_priority")
        
        # Apply type rules
        if message.message_type == UnifiedMessageType.ONBOARDING:
            rules_applied.append("onboarding_priority")
        elif message.message_type == UnifiedMessageType.BROADCAST:
            rules_applied.append("broadcast_routing")
        
        # Apply sender rules
        if message.sender_type == SenderType.CAPTAIN:
            rules_applied.append("captain_authority")
        
        # Apply recipient rules
        if message.recipient in self.routing_table:
            delivery_method = self.routing_table[message.recipient]
            rules_applied.append(f"recipient_routing_{delivery_method}")
        
        return {
            "strategy": strategy,
            "rules_applied": rules_applied,
            "delivery_priority": self._calculate_delivery_priority(message),
            "estimated_delivery_time": self._estimate_delivery_time(strategy)
        }
    
    def _calculate_delivery_priority(self, message: UnifiedMessage) -> int:
        """Calculate delivery priority score (higher = more urgent)."""
        priority_score = 0
        
        # Base priority
        if message.priority == UnifiedMessagePriority.URGENT:
            priority_score += 100
        else:
            priority_score += 50
        
        # Sender priority
        if message.sender_type == SenderType.CAPTAIN:
            priority_score += 50
        elif message.sender_type == SenderType.SYSTEM:
            priority_score += 25
        
        # Type priority
        if message.message_type == UnifiedMessageType.ONBOARDING:
            priority_score += 30
        elif message.message_type == UnifiedMessageType.BROADCAST:
            priority_score += 20
        
        return priority_score
    
    def _estimate_delivery_time(self, strategy: str) -> float:
        """Estimate delivery time based on strategy."""
        time_estimates = {
            "captain_priority": 0.1,
            "urgent_delivery": 0.2,
            "system_priority": 0.3,
            "broadcast_delivery": 1.0,
            "standard_delivery": 0.5
        }
        
        return time_estimates.get(strategy, 0.5)
    
    def _group_messages_by_strategy(self, messages: List[UnifiedMessage]) -> Dict[str, List[UnifiedMessage]]:
        """Group messages by coordination strategy."""
        grouped = {}
        
        for message in messages:
            strategy = self._determine_coordination_strategy(message)
            if strategy not in grouped:
                grouped[strategy] = []
            grouped[strategy].append(message)
        
        return grouped
    
    def _update_coordination_stats(self, success: bool, coordination_time: float):
        """Update coordination statistics."""
        self.coordination_stats["total_coordinations"] += 1
        
        if success:
            self.coordination_stats["successful_coordinations"] += 1
        else:
            self.coordination_stats["failed_coordinations"] += 1
        
        # Update average coordination time
        total = self.coordination_stats["total_coordinations"]
        current_avg = self.coordination_stats["average_coordination_time"]
        self.coordination_stats["average_coordination_time"] = (
            (current_avg * (total - 1) + coordination_time) / total
        )
    
    def get_coordination_stats(self) -> Dict[str, Any]:
        """Get coordination statistics."""
        stats = self.coordination_stats.copy()
        
        # Calculate success rate
        if stats["total_coordinations"] > 0:
            stats["success_rate"] = (
                stats["successful_coordinations"] / stats["total_coordinations"]
            )
        else:
            stats["success_rate"] = 0.0
        
        return stats
    
    def reset_stats(self):
        """Reset coordination statistics."""
        self.coordination_stats = {
            "total_coordinations": 0,
            "successful_coordinations": 0,
            "failed_coordinations": 0,
            "average_coordination_time": 0.0
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform coordination system health check."""
        try:
            return {
                "status": "healthy",
                "coordination_rules": len(self.coordination_rules),
                "routing_table": len(self.routing_table),
                "stats": self.get_coordination_stats()
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }