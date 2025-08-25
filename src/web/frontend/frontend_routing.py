#!/usr/bin/env python3
"""Frontend application routing and integration."""

import logging
import secrets
from datetime import datetime
from typing import Any, Dict

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from dataclasses import asdict

from .frontend_app_core import ComponentRegistry, StateManager, FrontendRoute
from .frontend_ui import register_default_components, process_component_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FlaskFrontendApp:
    """Flask-based frontend application."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = self.config.get("secret_key", secrets.token_hex(32))
        self.app.config["DEBUG"] = self.config.get("debug", False)

        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        CORS(self.app)

        self.component_registry = ComponentRegistry()
        self.state_manager = StateManager()

        self._setup_routes()
        self._setup_websocket_events()
        register_default_components(self.component_registry)

        logger.info("Flask frontend application initialized")

    def _setup_routes(self):
        """Setup Flask routes for frontend."""

        @self.app.route("/")
        def index():
            return render_template("frontend/index.html", app_name=self.state_manager.get_state().app_name)

        @self.app.route("/api/frontend/state")
        def get_state():
            return jsonify(asdict(self.state_manager.get_state()))

        @self.app.route("/api/frontend/components")
        def get_components():
            return jsonify(
                {
                    "components": self.component_registry.list_components(),
                    "templates": list(self.component_registry.templates.keys()),
                }
            )

        @self.app.route("/api/frontend/route/<path:route_path>")
        def get_route(route_path):
            return jsonify({"path": f"/{route_path}", "component": "PageComponent", "props": {}})

        @self.app.route("/api/frontend/theme", methods=["GET", "POST"])
        def theme_endpoint():
            if request.method == "POST":
                data = request.get_json()
                self.state_manager.update_state({"theme": data.get("theme", "light")})
                return jsonify({"status": "success"})
            return jsonify({"theme": self.state_manager.get_state().theme})

    def _setup_websocket_events(self):
        """Setup WebSocket events for real-time communication."""

        @self.socketio.on("connect")
        def handle_connect():
            logger.info(f"Client connected: {request.sid}")
            emit("connected", {"status": "connected", "sid": request.sid})

        @self.socketio.on("disconnect")
        def handle_disconnect():
            logger.info(f"Client disconnected: {request.sid}")

        @self.socketio.on("join_room")
        def handle_join_room(data):
            room = data.get("room")
            if room:
                join_room(room)
                emit("room_joined", {"room": room}, room=room)

        @self.socketio.on("state_update")
        def handle_state_update(data):
            try:
                self.state_manager.update_state(data)
                emit("state_changed", asdict(self.state_manager.get_state()), broadcast=True)
            except Exception as e:
                emit("error", {"message": str(e)})

        @self.socketio.on("component_event")
        def handle_component_event(data):
            component_id = data.get("component_id")
            event_type = data.get("event_type")
            event_data = data.get("event_data", {})

            process_component_event(self.state_manager, component_id, event_type, event_data)

            emit(
                "component_event_processed",
                {"component_id": component_id, "event_type": event_type, "event_data": event_data},
                broadcast=True,
            )

    def run(self, host: str = "127.0.0.1", port: int = 5000, debug: bool = False):
        """Run the Flask frontend application."""
        logger.info(f"Starting Flask frontend app on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)


class FastAPIFrontendApp:
    """FastAPI-based frontend application."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.app = FastAPI(
            title=self.config.get("title", "Agent_Cellphone_V2 Frontend API"),
            description=self.config.get("description", "Modern Frontend API with WebSocket Support"),
            version=self.config.get("version", "2.0.0"),
            docs_url="/docs",
            redoc_url="/redoc",
        )

        self._setup_middleware()

        self.component_registry = ComponentRegistry()
        self.state_manager = StateManager()

        self._setup_routes()
        self._setup_websocket_endpoints()
        register_default_components(self.component_registry)

        logger.info("FastAPI frontend application initialized")

    def _setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def index():
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{self.state_manager.get_state().app_name}</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                <div id="app">
                    <h1>{self.state_manager.get_state().app_name}</h1>
                    <p>FastAPI Frontend Application</p>
                </div>
            </body>
            </html>
            """

        @self.app.get("/api/frontend/state")
        async def get_state():
            return asdict(self.state_manager.get_state())

        @self.app.get("/api/frontend/components")
        async def get_components():
            return {
                "components": self.component_registry.list_components(),
                "templates": list(self.component_registry.templates.keys()),
            }

        @self.app.post("/api/frontend/state")
        async def update_state(updates: Dict[str, Any]):
            try:
                self.state_manager.update_state(updates)
                return {"status": "success", "message": "State updated"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

    def _setup_websocket_endpoints(self):
        @self.app.websocket("/ws/frontend")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            try:
                while True:
                    data = await websocket.receive_json()
                    message_type = data.get("type")

                    if message_type == "state_update":
                        self.state_manager.update_state(data.get("data", {}))
                        await websocket.send_json(
                            {"type": "state_changed", "data": asdict(self.state_manager.get_state())}
                        )
                    elif message_type == "component_event":
                        component_id = data.get("component_id")
                        event_type = data.get("event_type")
                        event_data = data.get("event_data", {})

                        process_component_event(self.state_manager, component_id, event_type, event_data)

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
                        await websocket.send_json({"type": "pong"})
            except WebSocketDisconnect:
                logger.info("WebSocket client disconnected")
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await websocket.send_json({"type": "error", "message": str(e)})


def create_route(
    path: str,
    name: str,
    component: str,
    props: Dict[str, Any] = None,
    meta: Dict[str, Any] = None,
) -> FrontendRoute:
    """Create a new frontend route."""
    return FrontendRoute(
        path=path,
        name=name,
        component=component,
        props=props or {},
        meta=meta or {},
        children=[],
    )


__all__ = ["FlaskFrontendApp", "FastAPIFrontendApp", "create_route"]
