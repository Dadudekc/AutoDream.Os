#!/usr/bin/env python3
"""
Unified Web Portal Architecture
Agent_Cellphone_V2_Repository - Multi-Agent Web Integration

This module implements the unified web portal that serves as the central
interface for all agent systems, providing navigation, dashboards, and
integration points.
"""

import json
import logging
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import uuid

from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Import cross-agent communication
try:
    from ..integration import (
        CrossAgentCommunicator,
        AgentMessage,
        AgentStatus,
        create_agent_communicator,
        MESSAGE_TYPES,
        COMMAND_CATEGORIES,
    )

    INTEGRATION_AVAILABLE = True
except ImportError:
    INTEGRATION_AVAILABLE = False
    CrossAgentCommunicator = None
    AgentMessage = None
    AgentStatus = None
    create_agent_communicator = None
    MESSAGE_TYPES = {}
    COMMAND_CATEGORIES = {}


class PortalSection(Enum):
    """Portal navigation sections"""

    DASHBOARD = "dashboard"
    AGENTS = "agents"
    AUTOMATION = "automation"
    PROJECTS = "projects"
    COORDINATION = "coordination"
    SETTINGS = "settings"
    HELP = "help"


class AgentDashboard(Enum):
    """Agent-specific dashboard types"""

    PROJECT_MANAGEMENT = "project_management"
    COORDINATION = "coordination"
    WEB_DEVELOPMENT = "web_development"
    AUTOMATION = "automation"
    DATA_ANALYSIS = "data_analysis"
    SYSTEM_ADMIN = "system_admin"
    USER_INTERFACE = "user_interface"
    INTEGRATION = "integration"


@dataclass
class PortalConfig:
    """Portal configuration settings"""

    title: str = "Agent_Cellphone_V2 Unified Portal"
    version: str = "1.0.0"
    theme: str = "default"
    enable_real_time: bool = True
    enable_websockets: bool = True
    enable_agent_integration: bool = True
    max_agents: int = 8
    session_timeout: int = 3600
    debug_mode: bool = False


@dataclass
class AgentPortalInfo:
    """Information about an agent's portal integration"""

    agent_id: str
    name: str
    description: str
    dashboard_type: AgentDashboard
    capabilities: List[str]
    status: str
    last_seen: str
    integration_status: str
    web_interface_url: Optional[str] = None
    api_endpoints: List[str] = None
    custom_components: List[str] = None

    def __post_init__(self):
        if self.api_endpoints is None:
            self.api_endpoints = []
        if self.custom_components is None:
            self.custom_components = []
        if not self.last_seen:
            self.last_seen = datetime.utcnow().isoformat()


@dataclass
class PortalNavigation:
    """Portal navigation structure"""

    section_id: str
    title: str
    icon: str
    url: str
    children: List["PortalNavigation"] = None
    permissions: List[str] = None
    badge: Optional[str] = None
    active: bool = False

    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.permissions is None:
            self.permissions = []


class UnifiedPortal:
    """Main unified portal class"""

    def __init__(self, config: PortalConfig = None):
        self.config = config or PortalConfig()
        self.logger = self._setup_logging()
        self.agents = {}
        self.navigation = self._create_default_navigation()
        self.active_sessions = {}
        self.websocket_connections = {}

        # Initialize cross-agent communication if available
        if INTEGRATION_AVAILABLE and self.config.enable_agent_integration:
            self.communicator = create_agent_communicator(
                "Portal",
                {
                    "secret_key": "portal-secret-key",
                    "redis": {"enabled": True, "host": "localhost"},
                    "rabbitmq": {"enabled": True, "host": "localhost"},
                },
            )
            self._setup_agent_communication()
        else:
            self.communicator = None
            self.logger.warning("Cross-agent integration not available")

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the portal"""
        logger = logging.getLogger("UnifiedPortal")
        logger.setLevel(logging.DEBUG if self.config.debug_mode else logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _create_default_navigation(self) -> List[PortalNavigation]:
        """Create default portal navigation structure"""
        return [
            PortalNavigation(
                section_id="dashboard",
                title="Dashboard",
                icon="dashboard",
                url="/dashboard",
                permissions=["view"],
            ),
            PortalNavigation(
                section_id="agents",
                title="Agent Management",
                icon="people",
                url="/agents",
                permissions=["view", "manage"],
                children=[
                    PortalNavigation(
                        section_id="agent_overview",
                        title="Overview",
                        icon="list",
                        url="/agents/overview",
                        permissions=["view"],
                    ),
                    PortalNavigation(
                        section_id="agent_details",
                        title="Details",
                        icon="info",
                        url="/agents/details",
                        permissions=["view"],
                    ),
                    PortalNavigation(
                        section_id="agent_integration",
                        title="Integration",
                        icon="link",
                        url="/agents/integration",
                        permissions=["manage"],
                    ),
                ],
            ),
            PortalNavigation(
                section_id="automation",
                title="Automation",
                icon="automation",
                url="/automation",
                permissions=["view", "execute"],
                children=[
                    PortalNavigation(
                        section_id="automation_workflows",
                        title="Workflows",
                        icon="workflow",
                        url="/automation/workflows",
                        permissions=["view", "execute"],
                    ),
                    PortalNavigation(
                        section_id="automation_tasks",
                        title="Tasks",
                        icon="task",
                        url="/automation/tasks",
                        permissions=["view", "execute"],
                    ),
                    PortalNavigation(
                        section_id="automation_monitoring",
                        title="Monitoring",
                        icon="monitor",
                        url="/automation/monitoring",
                        permissions=["view"],
                    ),
                ],
            ),
            PortalNavigation(
                section_id="projects",
                title="Projects",
                icon="project",
                url="/projects",
                permissions=["view", "manage"],
                children=[
                    PortalNavigation(
                        section_id="project_overview",
                        title="Overview",
                        icon="list",
                        url="/projects/overview",
                        permissions=["view"],
                    ),
                    PortalNavigation(
                        section_id="project_details",
                        title="Details",
                        icon="info",
                        url="/projects/details",
                        permissions=["view"],
                    ),
                    PortalNavigation(
                        section_id="project_coordination",
                        title="Coordination",
                        icon="coordinate",
                        url="/projects/coordination",
                        permissions=["manage"],
                    ),
                ],
            ),
            PortalNavigation(
                section_id="coordination",
                title="Coordination",
                icon="coordinate",
                url="/coordination",
                permissions=["view", "manage"],
                children=[
                    PortalNavigation(
                        section_id="coordination_overview",
                        title="Overview",
                        icon="list",
                        url="/coordination/overview",
                        permissions=["view"],
                    ),
                    PortalNavigation(
                        section_id="coordination_tasks",
                        title="Tasks",
                        icon="task",
                        url="/coordination/tasks",
                        permissions=["view", "manage"],
                    ),
                    PortalNavigation(
                        section_id="coordination_monitoring",
                        title="Monitoring",
                        icon="monitor",
                        url="/coordination/monitoring",
                        permissions=["view"],
                    ),
                ],
            ),
            PortalNavigation(
                section_id="settings",
                title="Settings",
                icon="settings",
                url="/settings",
                permissions=["manage"],
                children=[
                    PortalNavigation(
                        section_id="portal_settings",
                        title="Portal",
                        icon="portal",
                        url="/settings/portal",
                        permissions=["manage"],
                    ),
                    PortalNavigation(
                        section_id="agent_settings",
                        title="Agents",
                        icon="agent",
                        url="/settings/agents",
                        permissions=["manage"],
                    ),
                    PortalNavigation(
                        section_id="security_settings",
                        title="Security",
                        icon="security",
                        url="/settings/security",
                        permissions=["manage"],
                    ),
                ],
            ),
            PortalNavigation(
                section_id="help",
                title="Help & Support",
                icon="help",
                url="/help",
                permissions=["view"],
                children=[
                    PortalNavigation(
                        section_id="documentation",
                        title="Documentation",
                        icon="docs",
                        url="/help/documentation",
                        permissions=["view"],
                    ),
                    PortalNavigation(
                        section_id="troubleshooting",
                        title="Troubleshooting",
                        icon="troubleshoot",
                        url="/help/troubleshooting",
                        permissions=["view"],
                    ),
                    PortalNavigation(
                        section_id="support",
                        title="Support",
                        icon="support",
                        url="/help/support",
                        permissions=["view"],
                    ),
                ],
            ),
        ]

    def _setup_agent_communication(self):
        """Setup cross-agent communication handlers"""
        if not self.communicator:
            return

        # Register message handlers
        def handle_agent_status_update(message):
            """Handle agent status updates"""
            try:
                agent_data = message.payload
                agent_id = agent_data.get("agent_id")
                if agent_id:
                    self.update_agent_status(agent_id, agent_data)
                    return {"status": "updated"}
            except Exception as e:
                self.logger.error(f"Error handling agent status update: {e}")
                return {"status": "error", "message": str(e)}

        def handle_agent_integration_request(message):
            """Handle agent integration requests"""
            try:
                request_data = message.payload
                agent_id = request_data.get("agent_id")
                integration_type = request_data.get("integration_type")

                if agent_id and integration_type:
                    result = self.process_agent_integration(
                        agent_id, integration_type, request_data
                    )
                    return {"status": "processed", "result": result}
            except Exception as e:
                self.logger.error(f"Error handling integration request: {e}")
                return {"status": "error", "message": str(e)}

        # Register handlers
        self.communicator.register_message_handler("status", handle_agent_status_update)
        self.communicator.register_message_handler(
            "integration_request", handle_agent_integration_request
        )

        # Start listening
        self.communicator.start_listening()
        self.logger.info("Agent communication setup complete")

    def register_agent(self, agent_info: AgentPortalInfo) -> bool:
        """Register an agent with the portal"""
        try:
            self.agents[agent_info.agent_id] = agent_info
            self.logger.info(f"Registered agent: {agent_info.agent_id}")

            # Notify other agents about new registration
            if self.communicator:
                self.communicator.broadcast_message(
                    "agent_registered",
                    {
                        "agent_id": agent_info.agent_id,
                        "name": agent_info.name,
                        "dashboard_type": agent_info.dashboard_type.value,
                        "capabilities": agent_info.capabilities,
                    },
                    category="system",
                )

            return True
        except Exception as e:
            self.logger.error(f"Error registering agent {agent_info.agent_id}: {e}")
            return False

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the portal"""
        try:
            if agent_id in self.agents:
                del self.agents[agent_id]
                self.logger.info(f"Unregistered agent: {agent_id}")

                # Notify other agents about unregistration
                if self.communicator:
                    self.communicator.broadcast_message(
                        "agent_unregistered", {"agent_id": agent_id}, category="system"
                    )

                return True
            return False
        except Exception as e:
            self.logger.error(f"Error unregistering agent {agent_id}: {e}")
            return False

    def update_agent_status(self, agent_id: str, status_data: Dict[str, Any]) -> bool:
        """Update agent status information"""
        try:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agent.status = status_data.get("status", agent.status)
                agent.last_seen = datetime.utcnow().isoformat()

                # Update additional fields if provided
                if "capabilities" in status_data:
                    agent.capabilities = status_data["capabilities"]
                if "integration_status" in status_data:
                    agent.integration_status = status_data["integration_status"]

                self.logger.debug(f"Updated status for agent: {agent_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error updating agent status {agent_id}: {e}")
            return False

    def process_agent_integration(
        self, agent_id: str, integration_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process agent integration request"""
        try:
            if agent_id not in self.agents:
                return {"success": False, "error": "Agent not registered"}

            agent = self.agents[agent_id]

            if integration_type == "web_interface":
                # Handle web interface integration
                result = self._integrate_web_interface(agent, data)
            elif integration_type == "api_endpoints":
                # Handle API endpoint integration
                result = self._integrate_api_endpoints(agent, data)
            elif integration_type == "custom_components":
                # Handle custom component integration
                result = self._integrate_custom_components(agent, data)
            else:
                return {
                    "success": False,
                    "error": f"Unknown integration type: {integration_type}",
                }

            # Update agent integration status
            agent.integration_status = "integrated"

            return {"success": True, "result": result}

        except Exception as e:
            self.logger.error(f"Error processing integration for {agent_id}: {e}")
            return {"success": False, "error": str(e)}

    def _integrate_web_interface(
        self, agent: AgentPortalInfo, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Integrate agent web interface"""
        try:
            web_url = data.get("web_interface_url")
            if web_url:
                agent.web_interface_url = web_url
                return {"web_interface_url": web_url, "status": "integrated"}
            return {"status": "no_url_provided"}
        except Exception as e:
            self.logger.error(
                f"Error integrating web interface for {agent.agent_id}: {e}"
            )
            return {"status": "error", "message": str(e)}

    def _integrate_api_endpoints(
        self, agent: AgentPortalInfo, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Integrate agent API endpoints"""
        try:
            endpoints = data.get("api_endpoints", [])
            if endpoints:
                agent.api_endpoints = endpoints
                return {"api_endpoints": endpoints, "status": "integrated"}
            return {"status": "no_endpoints_provided"}
        except Exception as e:
            self.logger.error(
                f"Error integrating API endpoints for {agent.agent_id}: {e}"
            )
            return {"status": "error", "message": str(e)}

    def _integrate_custom_components(
        self, agent: AgentPortalInfo, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Integrate agent custom components"""
        try:
            components = data.get("custom_components", [])
            if components:
                agent.custom_components = components
                return {"custom_components": components, "status": "integrated"}
            return {"status": "no_components_provided"}
        except Exception as e:
            self.logger.error(
                f"Error integrating custom components for {agent.agent_id}: {e}"
            )
            return {"status": "error", "message": str(e)}

    def get_agent_info(self, agent_id: str) -> Optional[AgentPortalInfo]:
        """Get information about a specific agent"""
        return self.agents.get(agent_id)

    def get_all_agents(self) -> List[AgentPortalInfo]:
        """Get information about all registered agents"""
        return list(self.agents.values())

    def get_agents_by_type(
        self, dashboard_type: AgentDashboard
    ) -> List[AgentPortalInfo]:
        """Get agents by dashboard type"""
        return [
            agent
            for agent in self.agents.values()
            if agent.dashboard_type == dashboard_type
        ]

    def get_navigation(
        self, user_permissions: List[str] = None
    ) -> List[PortalNavigation]:
        """Get navigation structure filtered by user permissions"""
        if not user_permissions:
            user_permissions = ["view"]

        def filter_navigation(
            nav_items: List[PortalNavigation],
        ) -> List[PortalNavigation]:
            filtered = []
            for item in nav_items:
                # Check if user has required permissions
                if any(perm in user_permissions for perm in item.permissions):
                    # Create a copy to avoid modifying the original
                    filtered_item = PortalNavigation(
                        section_id=item.section_id,
                        title=item.title,
                        icon=item.icon,
                        url=item.url,
                        permissions=item.permissions.copy(),
                        badge=item.badge,
                        active=item.active,
                    )

                    # Filter children recursively
                    if item.children:
                        filtered_item.children = filter_navigation(item.children)

                    filtered.append(filtered_item)

            return filtered

        return filter_navigation(self.navigation)

    def create_session(self, user_id: str, permissions: List[str] = None) -> str:
        """Create a new user session"""
        session_id = str(uuid.uuid4())
        self.active_sessions[session_id] = {
            "user_id": user_id,
            "permissions": permissions or ["view"],
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
        }
        self.logger.info(f"Created session for user: {user_id}")
        return session_id

    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate a user session"""
        if session_id in self.active_sessions:
            session_data = self.active_sessions[session_id]

            # Check if session has expired
            created_at = datetime.fromisoformat(session_data["created_at"])
            if (
                datetime.utcnow() - created_at
            ).total_seconds() > self.config.session_timeout:
                del self.active_sessions[session_id]
                return None

            # Update last activity
            session_data["last_activity"] = datetime.utcnow().isoformat()
            return session_data

        return None

    def end_session(self, session_id: str) -> bool:
        """End a user session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            self.logger.info(f"Ended session: {session_id}")
            return True
        return False

    def get_portal_stats(self) -> Dict[str, Any]:
        """Get portal statistics and status"""
        return {
            "total_agents": len(self.agents),
            "active_sessions": len(self.active_sessions),
            "websocket_connections": len(self.websocket_connections),
            "agent_types": {
                dashboard_type.value: len(self.get_agents_by_type(dashboard_type))
                for dashboard_type in AgentDashboard
            },
            "integration_status": {
                "integrated": len(
                    [
                        a
                        for a in self.agents.values()
                        if a.integration_status == "integrated"
                    ]
                ),
                "pending": len(
                    [
                        a
                        for a in self.agents.values()
                        if a.integration_status != "integrated"
                    ]
                ),
            },
            "portal_uptime": datetime.utcnow().isoformat(),
        }

    def cleanup_expired_sessions(self):
        """Clean up expired user sessions"""
        current_time = datetime.utcnow()
        expired_sessions = []

        for session_id, session_data in self.active_sessions.items():
            created_at = datetime.fromisoformat(session_data["created_at"])
            if (
                current_time - created_at
            ).total_seconds() > self.config.session_timeout:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            del self.active_sessions[session_id]

        if expired_sessions:
            self.logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")


# Flask Portal Application
class FlaskPortalApp:
    """Flask-based portal application"""

    def __init__(self, portal: UnifiedPortal, config: Dict[str, Any] = None):
        self.portal = portal
        self.config = config or {}
        self.app = Flask(__name__)
        self.app.config.update(self.config.get("flask", {}))

        if self.config.get("enable_websockets", True):
            self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        else:
            self.socketio = None

        CORS(self.app)
        self._setup_routes()
        self._setup_websocket_events()

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route("/")
        def index():
            """Portal home page"""
            return render_template("portal/index.html", portal=self.portal)

        @self.app.route("/dashboard")
        def dashboard():
            """Main dashboard"""
            return render_template("portal/dashboard.html", portal=self.portal)

        @self.app.route("/agents")
        def agents_overview():
            """Agents overview page"""
            return render_template("portal/agents/overview.html", portal=self.portal)

        @self.app.route("/agents/<agent_id>")
        def agent_details(agent_id):
            """Agent details page"""
            agent = self.portal.get_agent_info(agent_id)
            if agent:
                return render_template(
                    "portal/agents/details.html", portal=self.portal, agent=agent
                )
            return "Agent not found", 404

        @self.app.route("/api/portal/stats")
        def portal_stats():
            """Get portal statistics"""
            return jsonify(self.portal.get_portal_stats())

        @self.app.route("/api/agents")
        def api_agents():
            """Get all agents"""
            agents = self.portal.get_all_agents()
            return jsonify([asdict(agent) for agent in agents])

        @self.app.route("/api/agents/<agent_id>")
        def api_agent_details(agent_id):
            """Get specific agent details"""
            agent = self.portal.get_agent_info(agent_id)
            if agent:
                return jsonify(asdict(agent))
            return jsonify({"error": "Agent not found"}), 404

        @self.app.route("/api/agents/<agent_id>/integrate", methods=["POST"])
        def api_agent_integrate(agent_id):
            """Integrate an agent"""
            try:
                data = request.get_json()
                integration_type = data.get("integration_type")

                if not integration_type:
                    return jsonify({"error": "Missing integration_type"}), 400

                result = self.portal.process_agent_integration(
                    agent_id, integration_type, data
                )
                return jsonify(result)

            except Exception as e:
                return jsonify({"error": str(e)}), 500

    def _setup_websocket_events(self):
        """Setup WebSocket events"""
        if not self.socketio:
            return

        @self.socketio.on("connect")
        def handle_connect():
            """Handle client connection"""
            session_id = request.args.get("session_id")
            if session_id:
                join_room(session_id)
                self.portal.websocket_connections[request.sid] = session_id

        @self.socketio.on("disconnect")
        def handle_disconnect():
            """Handle client disconnection"""
            if request.sid in self.portal.websocket_connections:
                del self.portal.websocket_connections[request.sid]

        @self.socketio.on("get_agent_status")
        def handle_get_agent_status(data):
            """Handle agent status request"""
            agent_id = data.get("agent_id")
            if agent_id:
                agent = self.portal.get_agent_info(agent_id)
                if agent:
                    emit("agent_status", asdict(agent))
                else:
                    emit("agent_status", {"error": "Agent not found"})

    def run(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = None):
        """Run the Flask portal application"""
        debug = debug if debug is not None else self.config.get("debug", False)

        if self.socketio:
            self.socketio.run(self.app, host=host, port=port, debug=debug)
        else:
            self.app.run(host=host, port=port, debug=debug)


# FastAPI Portal Application
class FastAPIPortalApp:
    """FastAPI-based portal application"""

    def __init__(self, portal: UnifiedPortal, config: Dict[str, Any] = None):
        self.portal = portal
        self.config = config or {}
        self.app = FastAPI(
            title="Agent_Cellphone_V2 Unified Portal",
            version="1.0.0",
            description="Unified web portal for all agent systems",
        )

        self._setup_middleware()
        self._setup_routes()
        self._setup_websocket_endpoints()

    def _setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        """Setup FastAPI routes"""

        @self.app.get("/")
        async def index():
            """Portal home page"""
            return HTMLResponse(
                """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Agent_Cellphone_V2 Unified Portal</title>
            </head>
            <body>
                <h1>Agent_Cellphone_V2 Unified Portal</h1>
                <p>Welcome to the unified portal for all agent systems.</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
            </html>
            """
            )

        @self.app.get("/api/portal/stats")
        async def portal_stats():
            """Get portal statistics"""
            return self.portal.get_portal_stats()

        @self.app.get("/api/agents")
        async def api_agents():
            """Get all agents"""
            agents = self.portal.get_all_agents()
            return [asdict(agent) for agent in agents]

        @self.app.get("/api/agents/{agent_id}")
        async def api_agent_details(agent_id: str):
            """Get specific agent details"""
            agent = self.portal.get_agent_info(agent_id)
            if agent:
                return asdict(agent)
            raise HTTPException(status_code=404, detail="Agent not found")

    def _setup_websocket_endpoints(self):
        """Setup WebSocket endpoints"""

        @self.app.websocket("/ws/{session_id}")
        async def websocket_endpoint(websocket: WebSocket, session_id: str):
            """WebSocket endpoint for real-time communication"""
            await websocket.accept()

            try:
                while True:
                    data = await websocket.receive_text()
                    message = json.loads(data)

                    # Handle different message types
                    if message.get("type") == "get_agent_status":
                        agent_id = message.get("agent_id")
                        if agent_id:
                            agent = self.portal.get_agent_info(agent_id)
                            if agent:
                                await websocket.send_text(json.dumps(asdict(agent)))
                            else:
                                await websocket.send_text(
                                    json.dumps({"error": "Agent not found"})
                                )

            except WebSocketDisconnect:
                pass

    def run(self, host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
        """Run the FastAPI portal application"""
        import uvicorn

        uvicorn.run(
            "src.web.portal.unified_portal:FastAPIPortalApp().app",
            host=host,
            port=port,
            reload=reload,
        )


# Portal Factory
class PortalFactory:
    """Factory for creating portal applications"""

    @staticmethod
    def create_flask_portal(
        portal: UnifiedPortal, config: Dict[str, Any] = None
    ) -> FlaskPortalApp:
        """Create a Flask-based portal application"""
        return FlaskPortalApp(portal, config)

    @staticmethod
    def create_fastapi_portal(
        portal: UnifiedPortal, config: Dict[str, Any] = None
    ) -> FastAPIPortalApp:
        """Create a FastAPI-based portal application"""
        return FastAPIPortalApp(portal, config)

    @staticmethod
    def create_unified_portal(
        backend_type: str = "flask", config: Dict[str, Any] = None
    ) -> Union[FlaskPortalApp, FastAPIPortalApp]:
        """Create a unified portal with specified backend"""
        portal = UnifiedPortal(config.get("portal") if config else None)

        if backend_type.lower() == "fastapi":
            return PortalFactory.create_fastapi_portal(portal, config)
        else:
            return PortalFactory.create_flask_portal(portal, config)


# Utility functions
def create_portal(config: Dict[str, Any] = None) -> UnifiedPortal:
    """Create a new unified portal instance"""
    return UnifiedPortal(config)


def create_flask_portal_app(
    portal: UnifiedPortal, config: Dict[str, Any] = None
) -> FlaskPortalApp:
    """Create a Flask portal application"""
    return PortalFactory.create_flask_portal(portal, config)


def create_fastapi_portal_app(
    portal: UnifiedPortal, config: Dict[str, Any] = None
) -> FastAPIPortalApp:
    """Create a FastAPI portal application"""
    return PortalFactory.create_fastapi_portal(portal, config)


# Portal version and constants
__version__ = "1.0.0"
__all__ = [
    "UnifiedPortal",
    "PortalConfig",
    "AgentPortalInfo",
    "PortalNavigation",
    "PortalSection",
    "AgentDashboard",
    "FlaskPortalApp",
    "FastAPIPortalApp",
    "PortalFactory",
    "create_portal",
    "create_flask_portal_app",
    "create_fastapi_portal_app",
]
