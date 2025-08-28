#!/usr/bin/env python3
"""
Frontend Application Architecture
Agent_Cellphone_V2_Repository TDD Integration Project

This module provides a unified frontend application architecture that integrates
with both Flask and FastAPI backends, featuring:
- Component-based UI system
- Real-time communication
- State management
- Routing and navigation
- Responsive design integration

Author: Web Development & UI Framework Specialist
License: MIT
"""

import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .routes import register_flask_routes, register_fastapi_routes
from .settings import get_settings

# Configure logging
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


# ============================================================================
# FLASK FRONTEND INTEGRATION
# ============================================================================


class FlaskFrontendApp:
    """Flask-based frontend application"""

    def __init__(self, config: Dict[str, Any] | None = None):
        settings = get_settings()
        self.config = {**asdict(settings), **(config or {})}
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = self.config["secret_key"]
        self.app.config["DEBUG"] = self.config[
            "debug"
        ]  # SECURITY: Debug disabled by default

        # Initialize extensions
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        CORS(self.app)

        # Initialize managers
        self.component_registry = ComponentRegistry()
        self.state_manager = StateManager()

        # Setup routes and WebSocket events
        register_flask_routes(self.app, self.state_manager, self.component_registry)
        self._setup_websocket_events()
        self._register_default_components()

        logger.info("Flask frontend application initialized")

    def _setup_websocket_events(self):
        """Setup WebSocket events for real-time communication"""

        @self.socketio.on("connect")
        def handle_connect():
            """Handle client connection"""
            logger.info(f"Client connected: {request.sid}")
            emit("connected", {"status": "connected", "sid": request.sid})

        @self.socketio.on("disconnect")
        def handle_disconnect():
            """Handle client disconnection"""
            logger.info(f"Client disconnected: {request.sid}")

        @self.socketio.on("join_room")
        def handle_join_room(data):
            """Handle room joining"""
            room = data.get("room")
            if room:
                join_room(room)
                emit("room_joined", {"room": room}, room=room)

        @self.socketio.on("state_update")
        def handle_state_update(data):
            """Handle state updates from client"""
            try:
                self.state_manager.update_state(data)
                emit(
                    "state_changed",
                    asdict(self.state_manager.get_state()),
                    broadcast=True,
                )
            except Exception as e:
                emit("error", {"message": str(e)})

        @self.socketio.on("component_event")
        def handle_component_event(data):
            """Handle component events"""
            component_id = data.get("component_id")
            event_type = data.get("event_type")
            event_data = data.get("event_data", {})

            # Process component event
            self._process_component_event(component_id, event_type, event_data)

            # Broadcast to all clients
            emit(
                "component_event_processed",
                {
                    "component_id": component_id,
                    "event_type": event_type,
                    "event_data": event_data,
                },
                broadcast=True,
            )

    def _register_default_components(self):
        """Register default UI components"""

        # Register basic components
        self.component_registry.register_component(
            "Button",
            lambda props: {"type": "button", "text": props.get("text", "Button")},
            template='<button class="btn btn-primary">{{ text }}</button>',
            style=".btn { padding: 8px 16px; border-radius: 4px; }",
            script='function handleClick() { console.log("Button clicked"); }',
        )

        self.component_registry.register_component(
            "Card",
            lambda props: {
                "type": "card",
                "title": props.get("title", "Card"),
                "content": props.get("content", ""),
            },
            template='<div class="card"><div class="card-header">{{ title }}</div><div class="card-body">{{ content }}</div></div>',
            style=".card { border: 1px solid #ddd; border-radius: 8px; margin: 8px; }",
            script="",
        )

    def _process_component_event(
        self, component_id: str, event_type: str, event_data: Dict[str, Any]
    ):
        """Process component events"""
        logger.info(f"Processing component event: {component_id} - {event_type}")
        # This would typically involve more complex event processing logic

        # Update component state if needed
        if component_id in self.state_manager.get_state().components:
            component = self.state_manager.get_state().components[component_id]
            component.state.update(event_data)
            component.updated_at = datetime.now()

    def run(
        self, host: str = "127.0.0.1", port: int = 5000, debug: bool = False
    ):  # SECURITY: Localhost only
        """Run the Flask frontend application"""
        logger.info(f"Starting Flask frontend app on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)


# ============================================================================
# FASTAPI FRONTEND INTEGRATION
# ============================================================================


class FastAPIFrontendApp:
    """FastAPI-based frontend application"""

    def __init__(self, config: Dict[str, Any] | None = None):
        settings = get_settings()
        self.config = {**asdict(settings), **(config or {})}

        # Initialize FastAPI app
        self.app = FastAPI(
            title=self.config["title"],
            description=self.config["description"],
            version=self.config["version"],
            docs_url="/docs",
            redoc_url="/redoc",
        )

        # Setup middleware
        self._setup_middleware()

        # Initialize managers
        self.component_registry = ComponentRegistry()
        self.state_manager = StateManager()

        # Setup routes and WebSocket endpoints
        register_fastapi_routes(self.app, self.state_manager, self.component_registry)
        self._setup_websocket_endpoints()
        self._register_default_components()

        logger.info("FastAPI frontend application initialized")

    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_websocket_endpoints(self):
        """Setup WebSocket endpoints for real-time communication"""

        @self.app.websocket("/ws/frontend")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for frontend communication"""
            await websocket.accept()

            try:
                while True:
                    # Receive message from client
                    data = await websocket.receive_json()
                    message_type = data.get("type")

                    if message_type == "state_update":
                        # Handle state update
                        self.state_manager.update_state(data.get("data", {}))

                        # Send updated state back to client
                        await websocket.send_json(
                            {
                                "type": "state_changed",
                                "data": asdict(self.state_manager.get_state()),
                            }
                        )

                    elif message_type == "component_event":
                        # Handle component event
                        component_id = data.get("component_id")
                        event_type = data.get("event_type")
                        event_data = data.get("event_data", {})

                        self._process_component_event(
                            component_id, event_type, event_data
                        )

                        # Send confirmation back to client
                        await websocket.send_json(
                            {
                                "type": "component_event_processed",
                                "data": {
                                    "component_id": component_id,
                                    "event_type": event_type,
                                    "event_data": event_data,
                                },
                            }
                        )

                    elif message_type == "ping":
                        # Handle ping for connection health
                        await websocket.send_json({"type": "pong"})

            except WebSocketDisconnect:
                logger.info("WebSocket client disconnected")
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await websocket.send_json({"type": "error", "message": str(e)})

    def _register_default_components(self):
        """Register default UI components"""
        # Same as Flask version for consistency
        self.component_registry.register_component(
            "Button",
            lambda props: {"type": "button", "text": props.get("text", "Button")},
            template='<button class="btn btn-primary">{{ text }}</button>',
            style=".btn { padding: 8px 16px; border-radius: 4px; }",
            script='function handleClick() { console.log("Button clicked"); }',
        )

        self.component_registry.register_component(
            "Card",
            lambda props: {
                "type": "card",
                "title": props.get("title", "Card"),
                "content": props.get("content", ""),
            },
            template='<div class="card"><div class="card-header">{{ title }}</div><div class="card-body">{{ content }}</div></div>',
            style=".card { border: 1px solid #ddd; border-radius: 8px; margin: 8px; }",
            script="",
        )

    def _process_component_event(
        self, component_id: str, event_type: str, event_data: Dict[str, Any]
    ):
        """Process component events"""
        logger.info(f"Processing component event: {component_id} - {event_type}")
        # Same logic as Flask version

        if component_id in self.state_manager.get_state().components:
            component = self.state_manager.get_state().components[component_id]
            component.state.update(event_data)
            component.updated_at = datetime.now()


# ============================================================================
# FRONTEND APPLICATION FACTORY
# ============================================================================


class FrontendAppFactory:
    """Factory for creating frontend applications"""

    @staticmethod
    def create_flask_app(config: Dict[str, Any] = None) -> FlaskFrontendApp:
        """Create a Flask-based frontend application"""
        return FlaskFrontendApp(config)

    @staticmethod
    def create_fastapi_app(config: Dict[str, Any] = None) -> FastAPIFrontendApp:
        """Create a FastAPI-based frontend application"""
        return FastAPIFrontendApp(config)

    @staticmethod
    def create_unified_app(backend_type: str = "flask", config: Dict[str, Any] = None):
        """Create a unified frontend application"""
        if backend_type.lower() == "fastapi":
            return FrontendAppFactory.create_fastapi_app(config)
        else:
            return FrontendAppFactory.create_flask_app(config)


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


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Example usage
    config = {"debug": True, "secret_key": "development-secret-key"}

    # Create Flask frontend app
    flask_app = FrontendAppFactory.create_flask_app(config)

    # Create FastAPI frontend app
    fastapi_app = FrontendAppFactory.create_fastapi_app(config)

    print("Frontend applications created successfully!")
    print(f"Flask app: {flask_app}")
    print(f"FastAPI app: {fastapi_app}")
