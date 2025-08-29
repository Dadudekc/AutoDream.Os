"""API route registrations for the portal Flask app."""

from __future__ import annotations

from typing import Any, Dict

from flask import Flask, render_template, request

from . import services
from .responses import json_response, error_response


def register_routes(app: Flask, portal) -> None:
    """Register Flask routes for the portal."""

    @app.route("/")
    def index() -> Any:
        """Main portal page."""
        return render_template(
            "portal/index.html",
            title=portal.config.title,
            version=portal.config.version,
        )

    @app.route("/api/status")
    def api_status() -> Any:
        """Get portal status."""
        return json_response(services.get_status(portal))

    @app.route("/api/agents")
    def api_agents() -> Any:
        """Get all agents."""
        return json_response({"agents": services.get_agents(portal)})

    @app.route("/api/agents/<agent_id>")
    def api_agent_detail(agent_id: str) -> Any:
        """Get specific agent details."""
        agent = services.get_agent(portal, agent_id)
        if agent:
            return json_response(agent)
        return error_response("Agent not found", 404)

    @app.route("/api/navigation")
    def api_navigation() -> Any:
        """Get navigation state."""
        return json_response(services.get_navigation(portal))

    @app.route("/api/navigation/<section>")
    def api_navigate_to(section: str) -> Any:
        """Navigate to a portal section."""
        if services.navigate_to(portal, section):
            return json_response({"success": True, "section": section})
        return error_response("Invalid section", 400)

    @app.route("/api/sessions", methods=["POST"])
    def api_create_session() -> Any:
        """Create a new session."""
        data: Dict[str, Any] = request.get_json() or {}
        user_id = data.get("user_id")
        metadata = data.get("metadata", {})
        if not user_id:
            return error_response("user_id required", 400)
        try:
            session_id = services.create_session(portal, user_id, metadata)
            return json_response({"session_id": session_id, "success": True})
        except Exception:  # noqa: BLE001
            return error_response("Session creation failed", 500)

    @app.route("/api/sessions/<session_id>", methods=["GET"])
    def api_session_status(session_id: str) -> Any:
        """Get session status."""
        valid = services.validate_session(portal, session_id)
        return json_response({"valid": valid, "session_id": session_id})

    @app.route("/api/sessions/<session_id>", methods=["DELETE"])
    def api_terminate_session(session_id: str) -> Any:
        """Terminate a session."""
        success = services.terminate_session(portal, session_id)
        return json_response({"success": success, "session_id": session_id})

    @app.route("/api/statistics")
    def api_statistics() -> Any:
        """Get portal statistics."""
        return json_response(services.get_statistics(portal))

    @app.errorhandler(404)
    def not_found(_):  # type: ignore[override]
        return error_response("Not found", 404)

    @app.errorhandler(500)
    def internal_error(_):  # type: ignore[override]
        return error_response("Internal server error", 500)
