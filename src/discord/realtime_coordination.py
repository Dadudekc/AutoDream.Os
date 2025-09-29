#!/usr/bin/env python3
"""
Real-Time Coordination System for Phase 2.3 Enhanced Discord Integration

V2 Compliance: ≤400 lines, 3 classes, 10 functions
Purpose: Real-time swarm coordination through Discord with event processing
"""

import queue
import threading
import uuid
from collections import defaultdict, deque
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
    payload: dict[str, Any]
    timestamp: datetime
    priority: EventPriority
    expires_at: datetime | None = None
    processed: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "source_agent": self.source_agent,
            "target_agents": self.target_agents,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "processed": self.processed,
        }


class CoordinationHub:
    """Real-time swarm coordination hub with event processing"""

    def __init__(self, max_queue_size: int = 1000):
        """Initialize coordination hub"""
        self.max_queue_size = max_queue_size
        self.event_queue = queue.PriorityQueue(maxsize=max_queue_size)
        self.event_handlers: dict[EventType, list[Callable]] = defaultdict(list)
        self.active_agents: set[str] = set()
        self.event_history: deque = deque(maxlen=1000)  # Keep last 1000 events
        self.processing_thread = None
        self.running = False
        self.lock = threading.Lock()

    def start(self) -> None:
        """Start the coordination hub processing"""
        if self.running:
            return

        self.running = True
        self.processing_thread = threading.Thread(target=self._process_events, daemon=True)
        self.processing_thread.start()

    def stop(self) -> None:
        """Stop the coordination hub processing"""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5.0)

    def register_agent(self, agent_id: str) -> bool:
        """Register agent with coordination hub"""
        with self.lock:
            self.active_agents.add(agent_id)

            # Create agent join event
            event = CoordinationEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.AGENT_JOIN,
                source_agent=agent_id,
                target_agents=list(self.active_agents),
                payload={"agent_id": agent_id, "timestamp": datetime.utcnow().isoformat()},
                timestamp=datetime.utcnow(),
                priority=EventPriority.NORMAL,
            )

            self._queue_event(event)
            return True

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister agent from coordination hub"""
        with self.lock:
            if agent_id in self.active_agents:
                self.active_agents.remove(agent_id)

                # Create agent leave event
                event = CoordinationEvent(
                    event_id=str(uuid.uuid4()),
                    event_type=EventType.AGENT_LEAVE,
                    source_agent=agent_id,
                    target_agents=list(self.active_agents),
                    payload={"agent_id": agent_id, "timestamp": datetime.utcnow().isoformat()},
                    timestamp=datetime.utcnow(),
                    priority=EventPriority.NORMAL,
                )

                self._queue_event(event)
                return True
            return False

    def register_event_handler(self, event_type: EventType, handler: Callable) -> None:
        """Register event handler for specific event type"""
        self.event_handlers[event_type].append(handler)

    def broadcast_event(
        self,
        event_type: EventType,
        source_agent: str,
        payload: dict[str, Any],
        priority: EventPriority = EventPriority.NORMAL,
        expires_in: timedelta | None = None,
    ) -> str:
        """Broadcast event to all active agents"""
        event = CoordinationEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source_agent=source_agent,
            target_agents=list(self.active_agents),
            payload=payload,
            timestamp=datetime.utcnow(),
            priority=priority,
            expires_at=datetime.utcnow() + expires_in if expires_in else None,
        )

        return self._queue_event(event)

    def send_event(
        self,
        event_type: EventType,
        source_agent: str,
        target_agents: list[str],
        payload: dict[str, Any],
        priority: EventPriority = EventPriority.NORMAL,
        expires_in: timedelta | None = None,
    ) -> str:
        """Send event to specific agents"""
        # Validate target agents
        valid_targets = [agent for agent in target_agents if agent in self.active_agents]

        if not valid_targets:
            return None

        event = CoordinationEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source_agent=source_agent,
            target_agents=valid_targets,
            payload=payload,
            timestamp=datetime.utcnow(),
            priority=priority,
            expires_at=datetime.utcnow() + expires_in if expires_in else None,
        )

        return self._queue_event(event)

    def _queue_event(self, event: CoordinationEvent) -> str:
        """Queue event for processing"""
        try:
            # Use negative priority for max-heap behavior (higher priority first)
            priority_value = -event.priority.value
            self.event_queue.put((priority_value, event.timestamp, event))
            return event.event_id
        except queue.Full:
            print(f"Event queue full, dropping event {event.event_id}")
            return None

    def _process_events(self) -> None:
        """Process events from queue"""
        while self.running:
            try:
                # Get event with timeout
                priority, timestamp, event = self.event_queue.get(timeout=1.0)

                # Check if event has expired
                if event.expires_at and datetime.utcnow() > event.expires_at:
                    continue

                # Process event
                self._handle_event(event)

                # Mark as processed
                event.processed = True

                # Add to history
                with self.lock:
                    self.event_history.append(event)

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing event: {e}")

    def _handle_event(self, event: CoordinationEvent) -> None:
        """Handle specific event"""
        handlers = self.event_handlers.get(event.event_type, [])

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler: {e}")

    def get_event_history(
        self, event_type: EventType | None = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        """Get event history with optional filtering"""
        with self.lock:
            events = list(self.event_history)

        if event_type:
            events = [e for e in events if e.event_type == event_type]

        # Sort by timestamp (newest first)
        events.sort(key=lambda x: x.timestamp, reverse=True)

        # Return limited results
        return [event.to_dict() for event in events[:limit]]

    def get_agent_status(self) -> dict[str, Any]:
        """Get current agent status"""
        with self.lock:
            return {
                "active_agents": list(self.active_agents),
                "agent_count": len(self.active_agents),
                "queue_size": self.event_queue.qsize(),
                "total_events_processed": len(self.event_history),
            }


class EventDispatcher:
    """Event dispatching for swarm coordination"""

    def __init__(self, coordination_hub: CoordinationHub):
        """Initialize event dispatcher"""
        self.coordination_hub = coordination_hub
        self.dispatch_rules = self._load_dispatch_rules()

    def dispatch_task_assignment(
        self, source_agent: str, target_agent: str, task_data: dict[str, Any]
    ) -> str:
        """Dispatch task assignment event"""
        payload = {
            "task_id": task_data.get("task_id"),
            "task_title": task_data.get("task_title"),
            "priority": task_data.get("priority", "NORMAL"),
            "deadline": task_data.get("deadline"),
            "description": task_data.get("description"),
            "dependencies": task_data.get("dependencies", []),
            "assigned_by": source_agent,
            "assigned_at": datetime.utcnow().isoformat(),
        }

        return self.coordination_hub.send_event(
            EventType.TASK_ASSIGNMENT, source_agent, [target_agent], payload, EventPriority.HIGH
        )

    def dispatch_status_update(self, source_agent: str, status_data: dict[str, Any]) -> str:
        """Dispatch status update event"""
        payload = {
            "agent_id": source_agent,
            "status": status_data.get("status"),
            "current_task": status_data.get("current_task"),
            "progress": status_data.get("progress", 0),
            "next_action": status_data.get("next_action"),
            "notes": status_data.get("notes"),
            "timestamp": datetime.utcnow().isoformat(),
        }

        return self.coordination_hub.broadcast_event(
            EventType.STATUS_UPDATE, source_agent, payload, EventPriority.NORMAL
        )

    def dispatch_coordination_request(
        self, source_agent: str, target_agents: list[str], request_data: dict[str, Any]
    ) -> str:
        """Dispatch coordination request event"""
        payload = {
            "request_id": str(uuid.uuid4()),
            "request_type": request_data.get("request_type"),
            "description": request_data.get("description"),
            "priority": request_data.get("priority", "NORMAL"),
            "deadline": request_data.get("deadline"),
            "expected_response": request_data.get("expected_response"),
            "context": request_data.get("context", {}),
            "requested_by": source_agent,
            "requested_at": datetime.utcnow().isoformat(),
        }

        return self.coordination_hub.send_event(
            EventType.COORDINATION_REQUEST, source_agent, target_agents, payload, EventPriority.HIGH
        )

    def dispatch_system_alert(self, source_agent: str, alert_data: dict[str, Any]) -> str:
        """Dispatch system alert event"""
        payload = {
            "alert_id": str(uuid.uuid4()),
            "alert_type": alert_data.get("alert_type"),
            "severity": alert_data.get("severity", "NORMAL"),
            "message": alert_data.get("message"),
            "affected_agents": alert_data.get("affected_agents", []),
            "resolution_steps": alert_data.get("resolution_steps"),
            "alerted_by": source_agent,
            "alerted_at": datetime.utcnow().isoformat(),
        }

        return self.coordination_hub.broadcast_event(
            EventType.SYSTEM_ALERT, source_agent, payload, EventPriority.URGENT
        )

    def dispatch_emergency_broadcast(
        self, source_agent: str, emergency_data: dict[str, Any]
    ) -> str:
        """Dispatch emergency broadcast event"""
        payload = {
            "emergency_id": str(uuid.uuid4()),
            "emergency_type": emergency_data.get("emergency_type"),
            "description": emergency_data.get("description"),
            "immediate_actions": emergency_data.get("immediate_actions", []),
            "contact_info": emergency_data.get("contact_info"),
            "broadcast_by": source_agent,
            "broadcast_at": datetime.utcnow().isoformat(),
        }

        return self.coordination_hub.broadcast_event(
            EventType.EMERGENCY_BROADCAST, source_agent, payload, EventPriority.CRITICAL
        )

    def _load_dispatch_rules(self) -> dict[str, Any]:
        """Load dispatch rules and configuration"""
        return {
            "max_retries": 3,
            "retry_delay": 5,  # seconds
            "event_timeout": 300,  # seconds
            "batch_size": 10,
            "priority_weights": {
                EventPriority.LOW: 1,
                EventPriority.NORMAL: 2,
                EventPriority.HIGH: 3,
                EventPriority.URGENT: 4,
                EventPriority.CRITICAL: 5,
            },
        }


class StatusBroadcaster:
    """Real-time status broadcasting system"""

    def __init__(self, coordination_hub: CoordinationHub):
        """Initialize status broadcaster"""
        self.coordination_hub = coordination_hub
        self.status_cache: dict[str, dict[str, Any]] = {}
        self.broadcast_interval = 30  # seconds
        self.last_broadcast = datetime.utcnow()
        self.broadcast_thread = None
        self.running = False

    def start_broadcasting(self) -> None:
        """Start periodic status broadcasting"""
        if self.running:
            return

        self.running = True
        self.broadcast_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        self.broadcast_thread.start()

    def stop_broadcasting(self) -> None:
        """Stop periodic status broadcasting"""
        self.running = False
        if self.broadcast_thread:
            self.broadcast_thread.join(timeout=5.0)

    def update_agent_status(self, agent_id: str, status_data: dict[str, Any]) -> None:
        """Update agent status in cache"""
        self.status_cache[agent_id] = {
            **status_data,
            "last_updated": datetime.utcnow().isoformat(),
            "agent_id": agent_id,
        }

    def get_swarm_status(self) -> dict[str, Any]:
        """Get current swarm status"""
        return {
            "total_agents": len(self.status_cache),
            "active_agents": [
                agent_id
                for agent_id, data in self.status_cache.items()
                if self._is_agent_active(data)
            ],
            "agent_statuses": self.status_cache,
            "last_broadcast": self.last_broadcast.isoformat(),
            "coordination_hub_status": self.coordination_hub.get_agent_status(),
        }

    def _is_agent_active(self, agent_data: dict[str, Any]) -> bool:
        """Check if agent is currently active"""
        last_updated = datetime.fromisoformat(agent_data.get("last_updated", "1970-01-01"))
        return datetime.utcnow() - last_updated < timedelta(minutes=5)

    def _broadcast_loop(self) -> None:
        """Periodic broadcast loop"""
        while self.running:
            try:
                # Check if it's time to broadcast
                if datetime.utcnow() - self.last_broadcast >= timedelta(
                    seconds=self.broadcast_interval
                ):
                    self._broadcast_swarm_status()
                    self.last_broadcast = datetime.utcnow()

                # Sleep for a short interval
                threading.Event().wait(5)

            except Exception as e:
                print(f"Error in broadcast loop: {e}")

    def _broadcast_swarm_status(self) -> None:
        """Broadcast current swarm status"""
        swarm_status = self.get_swarm_status()

        # Broadcast to all agents
        self.coordination_hub.broadcast_event(
            EventType.SWARM_SYNC,
            "StatusBroadcaster",
            {"swarm_status": swarm_status, "broadcast_time": datetime.utcnow().isoformat()},
            EventPriority.LOW,
        )


# Example usage and testing
if __name__ == "__main__":
    # Initialize real-time coordination system
    coordination_hub = CoordinationHub()
    event_dispatcher = EventDispatcher(coordination_hub)
    status_broadcaster = StatusBroadcaster(coordination_hub)

    # Start coordination hub
    coordination_hub.start()
    status_broadcaster.start_broadcasting()

    # Register test agents
    coordination_hub.register_agent("Agent-2")
    coordination_hub.register_agent("Agent-3")
    coordination_hub.register_agent("Agent-6")

    # Test event dispatching
    task_data = {
        "task_id": "V3-012",
        "task_title": "Phase 2.3 Discord Integration",
        "priority": "HIGH",
        "description": "Implement enhanced Discord integration",
    }

    event_id = event_dispatcher.dispatch_task_assignment("Agent-2", "Agent-3", task_data)
    print(f"Task assignment dispatched: {event_id}")

    # Test status update
    status_data = {
        "status": "Active",
        "current_task": "Phase 2.3 Architecture Design",
        "progress": 75,
    }

    event_id = event_dispatcher.dispatch_status_update("Agent-2", status_data)
    print(f"Status update dispatched: {event_id}")

    # Test coordination request
    request_data = {
        "request_type": "consolidation_analysis",
        "description": "Need consolidation analysis for system duplications",
        "priority": "HIGH",
    }

    event_id = event_dispatcher.dispatch_coordination_request(
        "Agent-2", ["Agent-3", "Agent-8"], request_data
    )
    print(f"Coordination request dispatched: {event_id}")

    # Wait for processing
    import time

    time.sleep(2)

    # Get event history
    history = coordination_hub.get_event_history(limit=10)
    print(f"\nEvent History ({len(history)} events):")
    for event in history:
        print(f"- {event['event_type']}: {event['source_agent']} -> {event['target_agents']}")

    # Get swarm status
    swarm_status = status_broadcaster.get_swarm_status()
    print("\nSwarm Status:")
    print(f"- Active Agents: {swarm_status['active_agents']}")
    print(f"- Total Agents: {swarm_status['total_agents']}")

    # Stop coordination system
    status_broadcaster.stop_broadcasting()
    coordination_hub.stop()
