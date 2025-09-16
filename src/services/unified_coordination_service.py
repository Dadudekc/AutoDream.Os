#!/usr/bin/env python3
"""
Unified Coordination Service - Phase 2 Consolidation
====================================================

Consolidated coordination service combining all coordination functionality
from coordination/ directory into a single unified service.

Consolidated from:
- coordination/bulk_coordinator.py
- coordination/strategy_coordinator.py  
- coordination/stats_tracker.py

V2 Compliance: ≤400 lines, single responsibility coordination.

Author: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class UnifiedCoordinationService:
    """Unified coordination service combining all coordination functionality."""

    def __init__(self) -> None:
        """Initialize unified coordination service."""
        self.stats_tracker = StatsTracker()
        self.strategy_coordinator = StrategyCoordinator()
        self.bulk_coordinator = BulkCoordinator()
        
        logger.info("Unified Coordination Service initialized")

    def coordinate_bulk_operation(
        self, 
        messages: List[Dict[str, Any]], 
        strategy: str = "default"
    ) -> Dict[str, Any]:
        """Coordinate bulk message operations with strategy."""
        try:
            # Apply coordination strategy
            strategy_result = self.strategy_coordinator.apply_strategy(
                messages, strategy
            )
            
            # Execute bulk coordination
            bulk_result = self.bulk_coordinator.coordinate_messages(
                strategy_result["grouped_messages"]
            )
            
            # Track statistics
            self.stats_tracker.record_coordination_stats(
                len(messages), 
                bulk_result.get("success_count", 0)
            )
            
            return {
                "status": "success",
                "coordinated_messages": bulk_result["coordinated_messages"],
                "statistics": self.stats_tracker.get_current_stats()
            }
            
        except Exception as e:
            logger.exception("Bulk coordination failed: %s", e)
            return {"status": "error", "message": str(e)}

    def get_coordination_statistics(self) -> Dict[str, Any]:
        """Get current coordination statistics."""
        return self.stats_tracker.get_current_stats()

    def apply_coordination_strategy(
        self, 
        operation_type: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply specific coordination strategy."""
        return self.strategy_coordinator.determine_strategy(
            operation_type, context
        )


class StatsTracker:
    """Handles coordination statistics tracking and reporting."""

    def __init__(self) -> None:
        """Initialize stats tracker."""
        self.coordination_count = 0
        self.success_count = 0
        self.error_count = 0
        self.start_time = datetime.now()

    def record_coordination_stats(self, total: int, successful: int) -> None:
        """Record coordination statistics."""
        self.coordination_count += total
        self.success_count += successful
        self.error_count += (total - successful)
        
        logger.debug(
            "Coordination stats recorded: %d total, %d successful, %d errors",
            total, successful, total - successful
        )

    def get_current_stats(self) -> Dict[str, Any]:
        """Get current statistics."""
        runtime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "total_coordinations": self.coordination_count,
            "successful_coordinations": self.success_count,
            "failed_coordinations": self.error_count,
            "success_rate": (
                self.success_count / self.coordination_count 
                if self.coordination_count > 0 else 0
            ),
            "runtime_seconds": runtime
        }

    def reset_stats(self) -> None:
        """Reset all statistics."""
        self.coordination_count = 0
        self.success_count = 0
        self.error_count = 0
        self.start_time = datetime.now()
        
        logger.info("Coordination statistics reset")


class StrategyCoordinator:
    """Handles coordination strategy determination and application."""

    def __init__(self) -> None:
        """Initialize strategy coordinator."""
        self.strategies = {
            "default": self._default_strategy,
            "priority": self._priority_strategy,
            "batch": self._batch_strategy
        }

    def determine_strategy(
        self, 
        operation_type: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Determine appropriate coordination strategy."""
        strategy_name = context.get("strategy", "default")
        
        if strategy_name not in self.strategies:
            strategy_name = "default"
            
        return {
            "strategy": strategy_name,
            "recommendation": self.strategies[strategy_name](context)
        }

    def apply_strategy(
        self, 
        messages: List[Dict[str, Any]], 
        strategy: str = "default"
    ) -> Dict[str, Any]:
        """Apply coordination strategy to messages."""
        if strategy not in self.strategies:
            strategy = "default"
            
        return self.strategies[strategy]({"messages": messages})

    def _default_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Default coordination strategy."""
        messages = context.get("messages", [])
        return {
            "grouped_messages": [messages],
            "strategy_applied": "default",
            "execution_order": "sequential"
        }

    def _priority_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Priority-based coordination strategy."""
        messages = context.get("messages", [])
        
        # Group by priority
        priority_groups = {}
        for message in messages:
            priority = message.get("priority", "normal")
            if priority not in priority_groups:
                priority_groups[priority] = []
            priority_groups[priority].append(message)
            
        return {
            "grouped_messages": list(priority_groups.values()),
            "strategy_applied": "priority",
            "execution_order": "priority_descending"
        }

    def _batch_strategy(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Batch processing coordination strategy."""
        messages = context.get("messages", [])
        batch_size = context.get("batch_size", 10)
        
        # Group into batches
        batches = []
        for i in range(0, len(messages), batch_size):
            batches.append(messages[i:i + batch_size])
            
        return {
            "grouped_messages": batches,
            "strategy_applied": "batch",
            "execution_order": "parallel"
        }


class BulkCoordinator:
    """Handles bulk message coordination and grouping."""

    def __init__(self) -> None:
        """Initialize bulk coordinator."""
        self.coordination_history = []

    def coordinate_messages(
        self, 
        grouped_messages: List[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """Coordinate grouped messages."""
        coordinated_messages = []
        success_count = 0
        
        for group in grouped_messages:
            try:
                coordinated_group = self._coordinate_group(group)
                coordinated_messages.extend(coordinated_group)
                success_count += len(coordinated_group)
                
            except Exception as e:
                logger.error("Group coordination failed: %s", e)
                
        return {
            "coordinated_messages": coordinated_messages,
            "success_count": success_count,
            "total_groups": len(grouped_messages)
        }

    def _coordinate_group(self, group: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Coordinate a single group of messages."""
        coordinated_group = []
        
        for message in group:
            # Add coordination metadata
            coordinated_message = {
                **message,
                "coordinated_at": datetime.now().isoformat(),
                "coordination_id": f"coord_{len(self.coordination_history)}"
            }
            coordinated_group.append(coordinated_message)
            
        # Record coordination
        self.coordination_history.append({
            "group_size": len(group),
            "timestamp": datetime.now().isoformat()
        })
        
        return coordinated_group


# Example usage and testing
if __name__ == "__main__":
    # Initialize service
    service = UnifiedCoordinationService()
    
    # Example coordination
    sample_messages = [
        {"id": "msg1", "content": "Test message 1", "priority": "high"},
        {"id": "msg2", "content": "Test message 2", "priority": "normal"},
        {"id": "msg3", "content": "Test message 3", "priority": "low"}
    ]
    
    result = service.coordinate_bulk_operation(sample_messages, "priority")
    print(f"Coordination result: {result}")
    
    stats = service.get_coordination_statistics()
    print(f"Statistics: {stats}")
