"""
Real-Time Coordination System - V2 Compliant Main Interface
===========================================================

Main coordination interface using refactored core components.
Maintains backward compatibility while using V2 compliant modules.

Author: Agent-5 (Coordinator)
License: MIT
"""

import logging
from collections.abc import Callable
from typing import Any

from .realtime_coordination_advanced import RealTimeCoordinationAdvanced
from .realtime_coordination_core import (
    EventPriority,
    EventType,
    RealTimeCoordinationCore,
)


class RealTimeCoordination:
    """
    Main real-time coordination interface.
    Provides backward compatibility while using refactored core components.
    """

    def __init__(self):
        """Initialize the coordination system"""
        self.core = RealTimeCoordinationCore()
        self.advanced = RealTimeCoordinationAdvanced(self.core)
        self.logger = logging.getLogger(__name__)

    # Core operations (delegated to core)
    def register_agent(self, agent_id: str) -> bool:
        """Register an agent with the coordination system"""
        return self.core.register_agent(agent_id)

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the coordination system"""
        return self.core.unregister_agent(agent_id)

    def emit_event(
        self,
        event_type: EventType,
        source_agent: str,
        target_agents: list[str],
        payload: dict[str, Any] = None,
        priority: EventPriority = EventPriority.NORMAL,
    ) -> str:
        """Emit a coordination event"""
        return self.core.emit_event(event_type, source_agent, target_agents, payload, priority)

    def register_handler(self, event_type: EventType, handler: Callable) -> None:
        """Register an event handler"""
        self.core.register_handler(event_type, handler)

    def process_events(self, max_events: int = 10) -> int:
        """Process events from the queue"""
        return self.core.process_events(max_events)

    def get_active_agents(self) -> set[str]:
        """Get set of active agents"""
        return self.core.get_active_agents()

    def get_queue_size(self) -> int:
        """Get current queue size"""
        return self.core.get_queue_size()

    # Advanced operations (delegated to advanced)
    def start_coordination_service(self) -> bool:
        """Start the coordination service"""
        return self.advanced.start_coordination_service()

    def stop_coordination_service(self) -> bool:
        """Stop the coordination service"""
        return self.advanced.stop_coordination_service()

    def get_coordination_summary(self) -> dict[str, Any]:
        """Get comprehensive coordination summary"""
        return self.advanced.get_coordination_summary()

    def sync_swarm_state(self, agent_id: str, state_data: dict[str, Any]) -> bool:
        """Synchronize agent state with swarm"""
        return self.advanced.swarm_manager.sync_swarm_state(agent_id, state_data)

    def broadcast_to_swarm(
        self, source_agent: str, message: str, priority: EventPriority = EventPriority.NORMAL
    ) -> str:
        """Broadcast message to entire swarm"""
        return self.advanced.swarm_manager.broadcast_to_swarm(source_agent, message, priority)

    def request_coordination(
        self, requester: str, target_agent: str, request_type: str, details: dict[str, Any]
    ) -> str:
        """Request coordination between agents"""
        return self.advanced.swarm_manager.request_coordination(
            requester, target_agent, request_type, details
        )
