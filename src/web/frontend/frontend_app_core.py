#!/usr/bin/env python3
"""
Frontend Application Core Module
Agent_Cellphone_V2_Repository TDD Integration Project

This module contains the core frontend application logic, models, and managers
extracted from the monolithic frontend_app.py file.

Author: Agent-8 (Integration Enhancement Manager)
Contract: MODERATE-021 - Frontend App Modularization
License: MIT
"""

import json
import secrets
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

# Import utilities (commented out for testing)
# from src.utils.stability_improvements import stability_manager, safe_import
# from src.utils.unified_logging_manager import get_logger

# Mock logger for testing
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# ============================================================================
# FRONTEND MODELS & DATA STRUCTURES
# ============================================================================


@dataclass
class UIComponent:
    """Represents a UI component with its properties and state"""

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
    """Represents a frontend route with its configuration"""

    path: str
    name: str
    component: str
    props: Dict[str, Any]
    meta: Dict[str, Any]
    children: List["FrontendRoute"]


@dataclass
class FrontendState:
    """Global frontend application state"""

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
    """Registry for managing UI components"""

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
        """Register a new UI component"""
        self.components[name] = component_func
        if template:
            self.templates[name] = template
        if style:
            self.styles[name] = style
        if script:
            self.scripts[name] = script
        logger.info(f"Registered component: {name}")

    def get_component(self, name: str) -> Optional[Callable]:
        """Get a registered component"""
        return self.components.get(name)

    def list_components(self) -> List[str]:
        """List all registered components"""
        return list(self.components.keys())

    def get_template(self, name: str) -> Optional[str]:
        """Get component template"""
        return self.templates.get(name)

    def get_style(self, name: str) -> Optional[str]:
        """Get component style"""
        return self.styles.get(name)

    def get_script(self, name: str) -> Optional[str]:
        """Get component script"""
        return self.scripts.get(name)


class StateManager:
    """Manages frontend application state"""

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
        """Update application state"""
        for key, value in updates.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)

        self.state.updated_at = datetime.now()
        self.history.append(FrontendState(**asdict(self.state)))

        # Notify subscribers
        self._notify_subscribers()

    def subscribe(self, callback: Callable):
        """Subscribe to state changes"""
        self.subscribers.append(callback)

    def _notify_subscribers(self):
        """Notify all subscribers of state changes"""
        for callback in self.subscribers:
            try:
                callback(self.state)
            except Exception as e:
                logger.error(f"Error in state subscriber: {e}")

    def get_state(self) -> FrontendState:
        """Get current state"""
        return self.state

    def undo(self) -> bool:
        """Undo last state change"""
        if len(self.history) > 1:
            self.history.pop()  # Remove current state
            previous_state = self.history[-1]
            self.state = FrontendState(**asdict(previous_state))
            self._notify_subscribers()
            return True
        return False

    def add_notification(self, notification: Dict[str, Any]):
        """Add a new notification"""
        self.state.notifications.append(notification)
        self.update_state({"notifications": self.state.notifications})

    def clear_notifications(self):
        """Clear all notifications"""
        self.update_state({"notifications": []})

    def set_theme(self, theme: str):
        """Set application theme"""
        self.update_state({"theme": theme})

    def set_language(self, language: str):
        """Set application language"""
        self.update_state({"language": language})

    def set_current_route(self, route: str):
        """Set current route"""
        self.update_state({"current_route": route})


class EventProcessor:
    """Processes component events and state updates"""

    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.event_handlers: Dict[str, Callable] = {}

    def register_event_handler(self, event_type: str, handler: Callable):
        """Register an event handler"""
        self.event_handlers[event_type] = handler
        logger.info(f"Registered event handler for: {event_type}")

    def process_component_event(
        self, component_id: str, event_type: str, event_data: Dict[str, Any]
    ):
        """Process component events"""
        logger.info(f"Processing component event: {component_id} - {event_type}")

        # Update component state if needed
        if component_id in self.state_manager.get_state().components:
            component = self.state_manager.get_state().components[component_id]
            component.state.update(event_data)
            component.updated_at = datetime.now()

        # Call registered event handler if exists
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type](component_id, event_data)
            except Exception as e:
                logger.error(f"Error in event handler {event_type}: {e}")

    def process_state_update(self, updates: Dict[str, Any]):
        """Process state updates"""
        try:
            self.state_manager.update_state(updates)
            return {"status": "success", "message": "State updated"}
        except Exception as e:
            logger.error(f"Error updating state: {e}")
            return {"status": "error", "message": str(e)}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def create_component(
    component_type: str, props: Dict[str, Any], children: List[UIComponent] = None
) -> UIComponent:
    """Create a new UI component"""
    return UIComponent(
        id=str(uuid.uuid4()),
        type=component_type,
        props=props,
        state={},
        children=children or [],
        event_handlers={},
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def create_route(
    path: str,
    name: str,
    component: str,
    props: Dict[str, Any] = None,
    meta: Dict[str, Any] = None,
) -> FrontendRoute:
    """Create a new frontend route"""
    return FrontendRoute(
        path=path,
        name=name,
        component=component,
        props=props or {},
        meta=meta or {},
        children=[],
    )


def validate_component_props(props: Dict[str, Any], required_props: List[str]) -> bool:
    """Validate component properties"""
    for prop in required_props:
        if prop not in props:
            logger.warning(f"Required prop '{prop}' missing from component")
            return False
    return True


def sanitize_component_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize component data for security"""
    # Basic sanitization - remove potentially dangerous keys
    dangerous_keys = ["__class__", "__dict__", "__module__", "__bases__"]
    sanitized = {}
    
    for key, value in data.items():
        if key not in dangerous_keys:
            if isinstance(value, dict):
                sanitized[key] = sanitize_component_data(value)
            elif isinstance(value, list):
                sanitized[key] = [sanitize_component_data(item) if isinstance(item, dict) else item for item in value]
            else:
                sanitized[key] = value
    
    return sanitized


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Test the core module
    print("Frontend Application Core Module")
    print("=" * 40)
    
    # Test component creation
    component = create_component("Button", {"text": "Click me"})
    print(f"Created component: {component.type} with props: {component.props}")
    
    # Test route creation
    route = create_route("/test", "Test Page", "TestComponent")
    print(f"Created route: {route.path} -> {route.component}")
    
    # Test state manager
    state_manager = StateManager()
    print(f"Initial state: {state_manager.get_state().app_name}")
    
    # Test component registry
    registry = ComponentRegistry()
    registry.register_component("TestButton", lambda props: props)
    print(f"Registered components: {registry.list_components()}")
    
    print("Core module tests completed successfully!")
