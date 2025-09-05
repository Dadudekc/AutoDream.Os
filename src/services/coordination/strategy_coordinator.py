"""
Strategy Coordinator - V2 Compliant Module
=========================================

Handles coordination strategy determination and application.
Extracted from messaging_coordination_handler.py for V2 compliance.

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


class StrategyCoordinator:
    """
    Handles coordination strategy determination and application.
    
    Manages strategy selection, rule application,
    and coordination execution.
    """
    
    def __init__(self):
        """Initialize strategy coordinator."""
        self.coordination_rules = self._initialize_coordination_rules()
        self.routing_table = self._initialize_routing_table()
    
    def _initialize_coordination_rules(self) -> Dict[str, Any]:
        """Initialize coordination rules."""
        return {
            "priority_routing": {
                UnifiedMessagePriority.URGENT: "immediate",
                UnifiedMessagePriority.REGULAR: "standard"
            },
            "type_routing": {
                UnifiedMessageType.ONBOARDING: "system_priority",
                UnifiedMessageType.BROADCAST: "broadcast",
                UnifiedMessageType.AGENT_TO_AGENT: "standard",
                UnifiedMessageType.SYSTEM_TO_AGENT: "system_priority",
                UnifiedMessageType.HUMAN_TO_AGENT: "standard"
            },
            "sender_routing": {
                SenderType.CAPTAIN: "highest_priority",
                SenderType.SYSTEM: "system_priority",
                SenderType.AGENT: "standard",
                SenderType.HUMAN: "standard"
            }
        }
    
    def _initialize_routing_table(self) -> Dict[str, Any]:
        """Initialize routing table."""
        return {
            "captain_priority": {
                "delivery_method": "immediate",
                "retry_attempts": 3,
                "timeout": 5
            },
            "urgent_delivery": {
                "delivery_method": "priority",
                "retry_attempts": 2,
                "timeout": 10
            },
            "system_priority": {
                "delivery_method": "standard",
                "retry_attempts": 2,
                "timeout": 15
            },
            "broadcast_delivery": {
                "delivery_method": "batch",
                "retry_attempts": 1,
                "timeout": 30
            },
            "standard_delivery": {
                "delivery_method": "standard",
                "retry_attempts": 1,
                "timeout": 20
            }
        }
    
    def determine_coordination_strategy(self, message: UnifiedMessage) -> str:
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
    
    def apply_coordination_rules(self, message: UnifiedMessage, strategy: str) -> Dict[str, Any]:
        """Apply coordination rules based on strategy."""
        rules_applied = []
        
        # Apply priority rules
        if message.priority == UnifiedMessagePriority.URGENT:
            rules_applied.append("urgent_priority")
        
        # Apply type rules
        if message.message_type == UnifiedMessageType.ONBOARDING:
            rules_applied.append("onboarding_priority")
        elif message.message_type == UnifiedMessageType.BROADCAST:
            rules_applied.append("broadcast_priority")
        
        # Apply sender rules
        if message.sender_type == SenderType.CAPTAIN:
            rules_applied.append("captain_priority")
        elif message.sender_type == SenderType.SYSTEM:
            rules_applied.append("system_priority")
        
        # Get routing configuration
        routing_config = self.routing_table.get(strategy, {})
        
        return {
            "strategy": strategy,
            "rules_applied": rules_applied,
            "routing_config": routing_config,
            "estimated_delivery_time": self._estimate_delivery_time(strategy)
        }
    
    def _estimate_delivery_time(self, strategy: str) -> float:
        """Estimate delivery time for strategy."""
        time_estimates = {
            "captain_priority": 0.1,
            "urgent_delivery": 0.2,
            "system_priority": 0.3,
            "broadcast_delivery": 1.0,
            "standard_delivery": 0.5
        }
        
        return time_estimates.get(strategy, 0.5)
    
    def get_coordination_rules(self) -> Dict[str, Any]:
        """Get coordination rules."""
        return self.coordination_rules.copy()
    
    def get_routing_table(self) -> Dict[str, Any]:
        """Get routing table."""
        return self.routing_table.copy()
    
    def update_coordination_rule(self, rule_type: str, key: str, value: Any) -> bool:
        """Update coordination rule."""
        if rule_type in self.coordination_rules:
            self.coordination_rules[rule_type][key] = value
            return True
        return False
    
    def update_routing_config(self, strategy: str, config: Dict[str, Any]) -> bool:
        """Update routing configuration."""
        if strategy in self.routing_table:
            self.routing_table[strategy].update(config)
            return True
        return False
    
    def get_coordinator_status(self) -> Dict[str, Any]:
        """Get coordinator status."""
        return {
            'coordination_rules_count': len(self.coordination_rules),
            'routing_strategies_count': len(self.routing_table),
            'available_strategies': list(self.routing_table.keys())
        }
