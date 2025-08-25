#!/usr/bin/env python3
"""Core models and state management for the frontend application."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class UIComponent:
    """Represents a UI component with its properties and state."""

    id: str
    type: str
    props: Dict[str, Any]
    state: Dict[str, Any]
    children: List["UIComponent"]
    event_handlers: Dict[str, str]
    created_at: datetime
    updated_at: datetime


@dataclass
class FrontendRoute:
    """Represents a frontend route with its configuration."""

    path: str
    name: str
    component: str
    props: Dict[str, Any]
    meta: Dict[str, Any]
    children: List["FrontendRoute"]


@dataclass
class FrontendState:
    """Global frontend application state."""

    app_name: str
    version: str
    current_route: str
    user: Optional[Dict[str, Any]]
    theme: str
    language: str
    notifications: List[Dict[str, Any]]
    components: Dict[str, UIComponent]
    created_at: datetime
    updated_at: datetime


class ComponentRegistry:
    """Registry for managing UI components."""

    def __init__(self):
        self.components: Dict[str, Callable] = {}
        self.templates: Dict[str, str] = {}
        self.styles: Dict[str, str] = {}
        self.scripts: Dict[str, str] = {}

    def register_component(
        self,
        name: str,
        component_func: Callable,
        template: str = "",
        style: str = "",
        script: str = "",
    ):
        """Register a new UI component."""
        self.components[name] = component_func
        if template:
            self.templates[name] = template
        if style:
            self.styles[name] = style
        if script:
            self.scripts[name] = script
        logger.info(f"Registered component: {name}")

    def get_component(self, name: str) -> Optional[Callable]:
        """Get a registered component."""
        return self.components.get(name)

    def list_components(self) -> List[str]:
        """List all registered components."""
        return list(self.components.keys())


class StateManager:
    """Manages frontend application state."""

    def __init__(self):
        self.state = FrontendState(
            app_name="Agent_Cellphone_V2 Frontend",
            version="2.0.0",
            current_route="/",
            user=None,
            theme="light",
            language="en",
            notifications=[],
            components={},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.subscribers: List[Callable] = []
        self.history: List[FrontendState] = []

    def update_state(self, updates: Dict[str, Any]):
        """Update application state."""
        for key, value in updates.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)

        self.state.updated_at = datetime.now()
        self.history.append(FrontendState(**asdict(self.state)))
        self._notify_subscribers()

    def subscribe(self, callback: Callable):
        """Subscribe to state changes."""
        self.subscribers.append(callback)

    def _notify_subscribers(self):
        """Notify all subscribers of state changes."""
        for callback in self.subscribers:
            try:
                callback(self.state)
            except Exception as e:
                logger.error(f"Error in state subscriber: {e}")

    def get_state(self) -> FrontendState:
        """Get current state."""
        return self.state

    def undo(self) -> bool:
        """Undo last state change."""
        if len(self.history) > 1:
            self.history.pop()
            previous_state = self.history[-1]
            self.state = FrontendState(**asdict(previous_state))
            self._notify_subscribers()
            return True
        return False


__all__ = [
    "UIComponent",
    "FrontendRoute",
    "FrontendState",
    "ComponentRegistry",
    "StateManager",
]
