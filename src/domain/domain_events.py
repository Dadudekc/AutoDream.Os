"""
Domain Events - V2 Compliant (Simplified)
=========================================

Core domain events with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
import uuid

logger = logging.getLogger(__name__)


class EventType(Enum):
    """Event type enumeration."""
    SYSTEM = "system"
    AGENT = "agent"
    TASK = "task"
    USER = "user"


class EventPriority(Enum):
    """Event priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DomainEvent:
    """Base domain event structure."""
    event_id: str
    event_type: EventType
    event_name: str
    source: str
    data: Dict[str, Any] = field(default_factory=dict)
    priority: EventPriority = EventPriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None

    def __post_init__(self):
        if not self.event_id:
            self.event_id = str(uuid.uuid4())
        if not self.correlation_id:
            self.correlation_id = str(uuid.uuid4())


@dataclass
class SystemEvent(DomainEvent):
    """System-related domain event."""
    system_component: str = ""
    operation: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.SYSTEM


@dataclass
class AgentEvent(DomainEvent):
    """Agent-related domain event."""
    agent_id: str = ""
    agent_name: str = ""
    action: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.AGENT


@dataclass
class TaskEvent(DomainEvent):
    """Task-related domain event."""
    task_id: str = ""
    task_name: str = ""
    action: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.TASK


@dataclass
class UserEvent(DomainEvent):
    """User-related domain event."""
    user_id: str = ""
    user_name: str = ""
    action: str = ""

    def __post_init__(self):
        super().__post_init__()
        self.event_type = EventType.USER


class EventHandler:
    """Simple event handler for domain events."""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._event_history: List[DomainEvent] = []
    
    def register_handler(self, event_name: str, handler: Callable) -> None:
        """Register an event handler."""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)
        logger.debug(f"Handler registered for event: {event_name}")
    
    def unregister_handler(self, event_name: str, handler: Callable) -> None:
        """Unregister an event handler."""
        if event_name in self._handlers:
            if handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
                logger.debug(f"Handler unregistered for event: {event_name}")
    
    def publish_event(self, event: DomainEvent) -> None:
        """Publish a domain event."""
        self._event_history.append(event)
        
        if event.event_name in self._handlers:
            for handler in self._handlers[event.event_name]:
                try:
                    handler(event)
                    logger.debug(f"Event {event.event_name} handled successfully")
                except Exception as e:
                    logger.error(f"Error handling event {event.event_name}: {e}")
        
        logger.info(f"Event published: {event.event_name} from {event.source}")
    
    def get_event_history(self, event_type: Optional[EventType] = None) -> List[DomainEvent]:
        """Get event history, optionally filtered by type."""
        if event_type:
            return [event for event in self._event_history if event.event_type == event_type]
        return self._event_history.copy()
    
    def clear_history(self) -> None:
        """Clear event history."""
        self._event_history.clear()
        logger.info("Event history cleared")


class EventBus:
    """Simple event bus for domain events."""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_name: str, handler: Callable) -> None:
        """Subscribe to an event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
        logger.debug(f"Subscribed to event: {event_name}")
    
    def unsubscribe(self, event_name: str, handler: Callable) -> None:
        """Unsubscribe from an event."""
        if event_name in self._subscribers:
            if handler in self._subscribers[event_name]:
                self._subscribers[event_name].remove(handler)
                logger.debug(f"Unsubscribed from event: {event_name}")
    
    def publish(self, event: DomainEvent) -> None:
        """Publish an event to all subscribers."""
        if event.event_name in self._subscribers:
            for handler in self._subscribers[event.event_name]:
                try:
                    handler(event)
                    logger.debug(f"Event {event.event_name} published to subscriber")
                except Exception as e:
                    logger.error(f"Error publishing event {event.event_name}: {e}")
        
        logger.info(f"Event published: {event.event_name}")
    
    def get_subscriber_count(self, event_name: str) -> int:
        """Get the number of subscribers for an event."""
        return len(self._subscribers.get(event_name, []))


class EventStore:
    """Simple event store for domain events."""
    
    def __init__(self):
        self._events: List[DomainEvent] = []
        self._event_index: Dict[str, List[DomainEvent]] = {}
    
    def append_event(self, event: DomainEvent) -> None:
        """Append an event to the store."""
        self._events.append(event)
        
        # Index by event name
        if event.event_name not in self._event_index:
            self._event_index[event.event_name] = []
        self._event_index[event.event_name].append(event)
        
        logger.debug(f"Event stored: {event.event_name}")
    
    def get_events(self, event_name: Optional[str] = None) -> List[DomainEvent]:
        """Get events, optionally filtered by name."""
        if event_name:
            return self._event_index.get(event_name, []).copy()
        return self._events.copy()
    
    def get_events_by_type(self, event_type: EventType) -> List[DomainEvent]:
        """Get events by type."""
        return [event for event in self._events if event.event_type == event_type]
    
    def get_events_by_source(self, source: str) -> List[DomainEvent]:
        """Get events by source."""
        return [event for event in self._events if event.source == source]
    
    def clear_events(self) -> None:
        """Clear all events."""
        self._events.clear()
        self._event_index.clear()
        logger.info("Event store cleared")


# Global instances
event_handler = EventHandler()
event_bus = EventBus()
event_store = EventStore()


def publish_event(event: DomainEvent) -> None:
    """Convenience function to publish an event."""
    event_handler.publish_event(event)
    event_bus.publish(event)
    event_store.append_event(event)


def create_system_event(name: str, source: str, data: Dict[str, Any] = None, 
                       component: str = "", operation: str = "") -> SystemEvent:
    """Create a system event."""
    return SystemEvent(
        event_id=str(uuid.uuid4()),
        event_name=name,
        source=source,
        data=data or {},
        system_component=component,
        operation=operation
    )


def create_agent_event(name: str, source: str, data: Dict[str, Any] = None,
                      agent_id: str = "", agent_name: str = "", action: str = "") -> AgentEvent:
    """Create an agent event."""
    return AgentEvent(
        event_id=str(uuid.uuid4()),
        event_name=name,
        source=source,
        data=data or {},
        agent_id=agent_id,
        agent_name=agent_name,
        action=action
    )


def create_task_event(name: str, source: str, data: Dict[str, Any] = None,
                     task_id: str = "", task_name: str = "", action: str = "") -> TaskEvent:
    """Create a task event."""
    return TaskEvent(
        event_id=str(uuid.uuid4()),
        event_name=name,
        source=source,
        data=data or {},
        task_id=task_id,
        task_name=task_name,
        action=action
    )


def create_user_event(name: str, source: str, data: Dict[str, Any] = None,
                     user_id: str = "", user_name: str = "", action: str = "") -> UserEvent:
    """Create a user event."""
    return UserEvent(
        event_id=str(uuid.uuid4()),
        event_name=name,
        source=source,
        data=data or {},
        user_id=user_id,
        user_name=user_name,
        action=action
    )
