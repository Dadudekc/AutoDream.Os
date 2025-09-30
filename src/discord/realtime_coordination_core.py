"""
Real-Time Coordination System Core - V2 Compliant
================================================

Core coordination functionality refactored for V2 compliance.
Advanced operations moved to separate modules.

Author: Agent-5 (Coordinator)
License: MIT
"""

import queue
import threading
import uuid
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any


class EventType(Enum):
    """Types of coordination events"""

    TASK_ASSIGNMENT = "task_assignment"
    STATUS_UPDATE = "status_update"
    COORDINATION_REQUEST = "coordination_request"
    SYSTEM_ALERT = "system_alert"
    SWARM_SYNC = "swarm_sync"
    EMERGENCY_BROADCAST = "emergency_broadcast"
    AGENT_JOIN = "agent_join"
    AGENT_LEAVE = "agent_leave"


class EventPriority(Enum):
    """Event priority levels"""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


@dataclass
class CoordinationEvent:
    """Coordination event data structure"""

    event_id: str
    event_type: EventType
    source_agent: str
    target_agents: list[str]
    priority: EventPriority
    payload: dict[str, Any]
    timestamp: datetime
    ttl: timedelta = timedelta(minutes=30)


class EventQueue:
    """Thread-safe event queue with priority handling"""

    def __init__(self):
        """Initialize event queue"""
        self._queues = {
            EventPriority.CRITICAL: queue.PriorityQueue(),
            EventPriority.URGENT: queue.PriorityQueue(),
            EventPriority.HIGH: queue.PriorityQueue(),
            EventPriority.NORMAL: queue.PriorityQueue(),
            EventPriority.LOW: queue.PriorityQueue(),
        }
        self._lock = threading.Lock()

    def put(self, event: CoordinationEvent) -> None:
        """Add event to appropriate priority queue"""
        with self._lock:
            priority_value = event.priority.value
            self._queues[event.priority].put((priority_value, event.timestamp, event))

    def get(self, timeout: float = None) -> CoordinationEvent | None:
        """Get highest priority event"""
        with self._lock:
            # Check queues in priority order
            for priority in [
                EventPriority.CRITICAL,
                EventPriority.URGENT,
                EventPriority.HIGH,
                EventPriority.NORMAL,
                EventPriority.LOW,
            ]:
                try:
                    _, _, event = self._queues[priority].get(timeout=0.1)
                    return event
                except queue.Empty:
                    continue
            return None

    def size(self) -> int:
        """Get total queue size"""
        with self._lock:
            return sum(q.qsize() for q in self._queues.values())


class RealTimeCoordinationCore:
    """
    Core real-time coordination functionality.
    Provides basic event processing and agent management.
    """

    def __init__(self):
        """Initialize coordination core"""
        self.event_queue = EventQueue()
        self.active_agents = set()
        self.event_handlers = defaultdict(list)
        self.running = False
        self._lock = threading.Lock()

    def register_agent(self, agent_id: str) -> bool:
        """Register an agent with the coordination system"""
        with self._lock:
            if agent_id not in self.active_agents:
                self.active_agents.add(agent_id)
                self._emit_event(EventType.AGENT_JOIN, agent_id, [agent_id])
                return True
            return False

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the coordination system"""
        with self._lock:
            if agent_id in self.active_agents:
                self.active_agents.remove(agent_id)
                self._emit_event(EventType.AGENT_LEAVE, agent_id, [agent_id])
                return True
            return False

    def emit_event(
        self,
        event_type: EventType,
        source_agent: str,
        target_agents: list[str],
        payload: dict[str, Any] = None,
        priority: EventPriority = EventPriority.NORMAL,
    ) -> str:
        """Emit a coordination event"""
        event_id = str(uuid.uuid4())
        event = CoordinationEvent(
            event_id=event_id,
            event_type=event_type,
            source_agent=source_agent,
            target_agents=target_agents,
            priority=priority,
            payload=payload or {},
            timestamp=datetime.now(),
        )

        self.event_queue.put(event)
        return event_id

    def register_handler(self, event_type: EventType, handler: Callable) -> None:
        """Register an event handler"""
        self.event_handlers[event_type].append(handler)

    def process_events(self, max_events: int = 10) -> int:
        """Process events from the queue"""
        processed = 0
        for _ in range(max_events):
            event = self.event_queue.get(timeout=0.1)
            if event is None:
                break

            # Check if event is expired
            if datetime.now() - event.timestamp > event.ttl:
                continue

            # Process event with registered handlers
            handlers = self.event_handlers.get(event.event_type, [])
            for handler in handlers:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in event handler: {e}")

            processed += 1

        return processed

    def get_active_agents(self) -> set[str]:
        """Get set of active agents"""
        with self._lock:
            return self.active_agents.copy()

    def get_queue_size(self) -> int:
        """Get current queue size"""
        return self.event_queue.size()

    def _emit_event(
        self, event_type: EventType, source_agent: str, target_agents: list[str]
    ) -> None:
        """Internal method to emit events"""
        self.emit_event(event_type, source_agent, target_agents)
