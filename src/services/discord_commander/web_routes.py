#!/usr/bin/env python3
"""
Web Routes - Flask routes for Discord Commander Web Controller
==========================================================

Flask routes extracted from web_controller.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

from .web_handlers import WebHandlers
from .web_utils import create_template_data

logger = logging.getLogger(__name__)


class WebRoutes:
    """Flask routes for Discord Commander web interface."""

    def __init__(
        self, app: Flask, socketio: SocketIO, messaging_service=None, coordination_service=None
    ):
        """Initialize web routes."""
        self.app = app
        self.socketio = socketio
        self.handlers = WebHandlers(messaging_service, coordination_service)
        self._register_routes()
        self._register_socket_events()

    def _register_routes(self):
        """Register Flask routes."""

        @self.app.route("/")
        def index():
            """Main dashboard page."""
            try:
                template_data = create_template_data()
                return render_template("dashboard.html", **template_data.__dict__)
            except Exception as e:
                logger.error(f"Error rendering dashboard: {e}")
                return f"Error loading dashboard: {e}", 500

        @self.app.route("/api/agents")
        def get_agents():
            """Get all agents status."""
            result = self.handlers.handle_get_agents()
            return jsonify(result)

        @self.app.route("/api/send-message", methods=["POST"])
        def send_message():
            """Send message to agent."""
            result = self.handlers.handle_send_message()
            return jsonify(result)

        @self.app.route("/api/swarm-coordinate", methods=["POST"])
        def swarm_coordinate():
            """Handle swarm coordination request."""
            result = self.handlers.handle_swarm_coordinate()
            return jsonify(result)

        @self.app.route("/api/system-status")
        def get_system_status():
            """Get system status."""
            result = self.handlers.handle_get_system_status()
            return jsonify(result)

        @self.app.route("/api/social-media-status")
        def get_social_media_status():
            """Get social media status."""
            result = self.handlers.handle_get_social_media_status()
            return jsonify(result)

        @self.app.route("/api/post-to-social-media", methods=["POST"])
        def post_to_social_media():
            """Post to social media."""
            result = self.handlers.handle_post_to_social_media()
            return jsonify(result)

        @self.app.route("/api/quality-metrics")
        def get_quality_metrics():
            """Get quality metrics."""
            result = self.handlers.handle_get_quality_metrics()
            return jsonify(result)

        @self.app.route("/api/health")
        def health_check():
            """Health check endpoint."""
            result = self.handlers.handle_health_check()
            return jsonify(result)

    def _register_socket_events(self):
        """Register SocketIO events."""

        @self.socketio.on("connect")
        def handle_connect():
            """Handle client connection."""
            logger.info("Client connected to websocket")
            emit("status", {"message": "Connected to Discord Commander"})

        @self.socketio.on("disconnect")
        def handle_disconnect():
            """Handle client disconnection."""
            logger.info("Client disconnected from websocket")

        @self.socketio.on("get_agent_status")
        def handle_get_agent_status():
            """Handle agent status request via websocket."""
            try:
                result = self.handlers.handle_get_agents()
                emit("agent_status_response", result)
            except Exception as e:
                logger.error(f"Error handling agent status request: {e}")
                emit("error", {"message": str(e)})

        @self.socketio.on("get_social_status")
        def handle_get_social_status():
            """Handle social media status request via websocket."""
            try:
                result = self.handlers.handle_get_social_media_status()
                emit("social_status_response", result)
            except Exception as e:
                logger.error(f"Error handling social status request: {e}")
                emit("error", {"message": str(e)})

        @self.socketio.on("send_message")
        def handle_send_message(data):
            """Handle send message request via websocket."""
            try:
                # Simulate request object for handlers
                class MockRequest:
                    def get_json(self):
                        return data

                original_request = request
                request.get_json = MockRequest().get_json

                result = self.handlers.handle_send_message()

                # Restore original request
                request.get_json = original_request.get_json

                emit("message_response", result)
            except Exception as e:
                logger.error(f"Error handling send message request: {e}")
                emit("error", {"message": str(e)})

        @self.socketio.on("get_system_status")
        def handle_get_system_status():
            """Handle system status request via websocket."""
            try:
                result = self.handlers.handle_get_system_status()
                emit("system_status_response", result)
            except Exception as e:
                logger.error(f"Error handling system status request: {e}")
                emit("error", {"message": str(e)})

        @self.socketio.on("update_dashboard")
        def handle_update_dashboard():
            """Handle dashboard update request via websocket."""
            try:
                template_data = create_template_data()
                emit("dashboard_update", template_data.__dict__)
            except Exception as e:
                logger.error(f"Error handling dashboard update: {e}")
                emit("error", {"message": str(e)})

    def broadcast_agent_update(self, agent_id: str, status_data: dict):
        """Broadcast agent status update to all connected clients."""
        try:
            self.socketio.emit(
                "agent_status_update",
                {
                    "agent_id": agent_id,
                    "status_data": status_data,
                    "timestamp": status_data.get("last_updated", ""),
                },
            )
        except Exception as e:
            logger.error(f"Error broadcasting agent update: {e}")

    def broadcast_system_update(self, system_data: dict):
        """Broadcast system status update to all connected clients."""
        try:
            self.socketio.emit(
                "system_status_update",
                {"system_data": system_data, "timestamp": system_data.get("timestamp", "")},
            )
        except Exception as e:
            logger.error(f"Error broadcasting system update: {e}")

    def broadcast_message_notification(self, message_data: dict):
        """Broadcast message notification to all connected clients."""
        try:
            self.socketio.emit(
                "message_notification",
                {"message_data": message_data, "timestamp": message_data.get("timestamp", "")},
            )
        except Exception as e:
            logger.error(f"Error broadcasting message notification: {e}")
