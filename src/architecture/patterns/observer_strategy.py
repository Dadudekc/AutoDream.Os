#!/usr/bin/env python3
"""
Observer and Strategy Patterns - V2 Compliant
==============================================

Observer and Strategy pattern implementations for the Agent Cellphone V2 project.
Maintains V2 compliance with focused responsibility.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
import threading
from typing import Any, Dict, List, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from ...core.shared_logging import get_module_logger

logger = get_module_logger(__name__)


@dataclass
class Event:
    """Base event class."""
    event_type: str
    source: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__('time').time())


class Observer:
    """Observer interface."""
    
    def update(self, event: Event) -> None:
        """Handle event update."""
        pass


class Subject:
    """Subject for observer pattern."""
    
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()
    
    def attach(self, observer: Observer) -> None:
        """Attach observer."""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)
                logger.debug(f"Observer attached: {type(observer).__name__}")
    
    def detach(self, observer: Observer) -> None:
        """Detach observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
                logger.debug(f"Observer detached: {type(observer).__name__}")
    
    def notify(self, event: Event) -> None:
        """Notify all observers."""
        with self._lock:
            for observer in self._observers:
                try:
                    observer.update(event)
                except Exception as e:
                    logger.error(f"Observer notification failed: {e}")
    
    def get_observer_count(self) -> int:
        """Get number of observers."""
        with self._lock:
            return len(self._observers)


class ValidationStrategy:
    """Validation strategy interface."""
    
    def validate(self, data: Any) -> bool:
        """Validate data."""
        return True


class MessageValidationStrategy(ValidationStrategy):
    """Message validation strategy."""
    
    def validate(self, data: Any) -> bool:
        """Validate message data."""
        return isinstance(data, str) and len(data.strip()) > 0


class AgentValidationStrategy(ValidationStrategy):
    """Agent validation strategy."""
    
    def validate(self, data: Any) -> bool:
        """Validate agent data."""
        return isinstance(data, str) and data.startswith("Agent-")


class EmailValidationStrategy(ValidationStrategy):
    """Email validation strategy."""
    
    def validate(self, data: Any) -> bool:
        """Validate email data."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return isinstance(data, str) and bool(re.match(pattern, data))


class ValidationContext:
    """Validation context using strategy pattern."""
    
    def __init__(self, strategy: ValidationStrategy = None):
        self._strategy = strategy or ValidationStrategy()
    
    def set_strategy(self, strategy: ValidationStrategy) -> None:
        """Set validation strategy."""
        self._strategy = strategy
    
    def validate(self, data: Any) -> bool:
        """Validate using current strategy."""
        return self._strategy.validate(data)
    
    def get_strategy_type(self) -> str:
        """Get current strategy type."""
        return type(self._strategy).__name__


class EventBus:
    """Simple event bus for domain events."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to event type."""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
            logger.debug(f"Subscribed to event: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from event type."""
        with self._lock:
            if event_type in self._subscribers:
                if callback in self._subscribers[event_type]:
                    self._subscribers[event_type].remove(callback)
                    logger.debug(f"Unsubscribed from event: {event_type}")
    
    def publish(self, event: Event) -> None:
        """Publish event to subscribers."""
        with self._lock:
            if event.event_type in self._subscribers:
                for callback in self._subscribers[event.event_type]:
                    try:
                        callback(event)
                    except Exception as e:
                        logger.error(f"Event callback failed: {e}")
    
    def get_subscriber_count(self, event_type: str) -> int:
        """Get subscriber count for event type."""
        with self._lock:
            return len(self._subscribers.get(event_type, []))
    
    def list_event_types(self) -> List[str]:
        """List all event types."""
        with self._lock:
            return list(self._subscribers.keys())


class StrategyFactory:
    """Factory for creating validation strategies."""
    
    _strategies = {
        "message": MessageValidationStrategy,
        "agent": AgentValidationStrategy,
        "email": EmailValidationStrategy
    }
    
    @classmethod
    def create_strategy(cls, strategy_type: str) -> ValidationStrategy:
        """Create validation strategy."""
        if strategy_type not in cls._strategies:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
        
        return cls._strategies[strategy_type]()
    
    @classmethod
    def register_strategy(cls, strategy_type: str, strategy_class: type) -> None:
        """Register new strategy type."""
        cls._strategies[strategy_type] = strategy_class
    
    @classmethod
    def list_strategies(cls) -> List[str]:
        """List available strategies."""
        return list(cls._strategies.keys())


