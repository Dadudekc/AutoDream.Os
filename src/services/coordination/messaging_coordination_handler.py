"""
Messaging Coordination Handler - V2 Compliant Module
===================================================

Main coordination handler for messaging operations.
Coordinates all coordination components and provides unified interface.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Any, Dict, List, Optional
from ..models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    SenderType,
    RecipientType
)
from .strategy_coordinator import StrategyCoordinator
from .bulk_coordinator import BulkCoordinator
from .stats_tracker import StatsTracker


class MessagingCoordinationHandler:
    """
    Main coordination handler for messaging operations.
    
    Coordinates strategy determination, bulk processing,
    and statistics tracking for messaging operations.
    """
    
    def __init__(self):
        """Initialize coordination handler."""
        self.strategy_coordinator = StrategyCoordinator()
        self.bulk_coordinator = BulkCoordinator()
        self.stats_tracker = StatsTracker()
    
    def coordinate_message(self, message: UnifiedMessage) -> Dict[str, Any]:
        """
        Coordinate a single message for delivery.
        
        Args:
            message: Message to coordinate
            
        Returns:
            Coordination result dictionary
        """
        start_time = time.time()
        
        try:
            # Determine coordination strategy
            strategy = self.strategy_coordinator.determine_coordination_strategy(message)
            
            # Apply coordination rules
            coordination_result = self.strategy_coordinator.apply_coordination_rules(message, strategy)
            
            # Update statistics
            self.stats_tracker.update_coordination_stats(
                True, time.time() - start_time, strategy,
                message.priority.value, message.message_type.value, message.sender_type.value
            )
            
            return {
                "success": True,
                "strategy": strategy,
                "coordination_result": coordination_result,
                "message_id": message.message_id,
                "recipient": message.recipient
            }
            
        except Exception as e:
            self.stats_tracker.update_coordination_stats(
                False, time.time() - start_time,
                message.priority.value, message.message_type.value, message.sender_type.value
            )
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
        return self.bulk_coordinator.coordinate_bulk_messages(messages)
    
    def coordinate_messages_by_priority(self, messages: List[UnifiedMessage]) -> Dict[str, Any]:
        """Coordinate messages grouped by priority."""
        return self.bulk_coordinator.coordinate_messages_by_priority(messages)
    
    def coordinate_messages_by_type(self, messages: List[UnifiedMessage]) -> Dict[str, Any]:
        """Coordinate messages grouped by type."""
        return self.bulk_coordinator.coordinate_messages_by_type(messages)
    
    def coordinate_messages_by_sender(self, messages: List[UnifiedMessage]) -> Dict[str, Any]:
        """Coordinate messages grouped by sender type."""
        return self.bulk_coordinator.coordinate_messages_by_sender(messages)
    
    def get_coordination_stats(self) -> Dict[str, Any]:
        """Get coordination statistics."""
        return self.stats_tracker.get_coordination_stats()
    
    def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed statistics."""
        return self.stats_tracker.get_detailed_stats()
    
    def get_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for specified hours."""
        return self.stats_tracker.get_performance_summary(hours)
    
    def reset_stats(self):
        """Reset coordination statistics."""
        self.stats_tracker.reset_stats()
    
    def health_check(self) -> Dict[str, Any]:
        """Perform coordination system health check."""
        try:
            return {
                "status": "healthy",
                "coordination_rules": len(self.strategy_coordinator.get_coordination_rules()),
                "routing_table": len(self.strategy_coordinator.get_routing_table()),
                "stats": self.get_coordination_stats(),
                "component_status": {
                    "strategy_coordinator": self.strategy_coordinator.get_coordinator_status(),
                    "bulk_coordinator": self.bulk_coordinator.get_bulk_coordinator_status(),
                    "stats_tracker": self.stats_tracker.get_tracker_status()
                }
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def get_coordination_rules(self) -> Dict[str, Any]:
        """Get coordination rules."""
        return self.strategy_coordinator.get_coordination_rules()
    
    def get_routing_table(self) -> Dict[str, Any]:
        """Get routing table."""
        return self.strategy_coordinator.get_routing_table()
    
    def update_coordination_rule(self, rule_type: str, key: str, value: Any) -> bool:
        """Update coordination rule."""
        return self.strategy_coordinator.update_coordination_rule(rule_type, key, value)
    
    def update_routing_config(self, strategy: str, config: Dict[str, Any]) -> bool:
        """Update routing configuration."""
        return self.strategy_coordinator.update_routing_config(strategy, config)
    
    def get_handler_status(self) -> Dict[str, Any]:
        """Get handler status."""
        return {
            'coordination_stats': self.get_coordination_stats(),
            'health_status': self.health_check(),
            'component_status': {
                'strategy_coordinator': self.strategy_coordinator.get_coordinator_status(),
                'bulk_coordinator': self.bulk_coordinator.get_bulk_coordinator_status(),
                'stats_tracker': self.stats_tracker.get_tracker_status()
            }
        }
