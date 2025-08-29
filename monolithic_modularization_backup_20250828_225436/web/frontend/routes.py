from typing import Any, Dict, TYPE_CHECKING

from fastapi import FastAPI
from flask import Flask, jsonify, request

    from .frontend_app import ComponentRegistry, StateManager
from . import controllers
from __future__ import annotations
from fastapi.responses import HTMLResponse

"""Route definitions for different web frameworks."""





if TYPE_CHECKING:  # pragma: no cover - used only for type hints


def register_flask_routes(
    app: Flask, state_manager: "StateManager", registry: "ComponentRegistry"
) -> None:
    """Attach route handlers to a Flask ``app``."""

    @app.route("/")
    def index() -> str:
        return controllers.render_index(state_manager)

    @app.route("/api/frontend/state")
    def get_state() -> Any:
        return jsonify(controllers.current_state(state_manager))

    @app.route("/api/frontend/components")
    def get_components() -> Any:
        return jsonify(controllers.component_listing(registry))

    @app.route("/api/frontend/route/<path:route_path>")
    def get_route(route_path: str) -> Any:
        return jsonify(controllers.route_info(route_path))

    @app.route("/api/frontend/theme", methods=["GET", "POST"])
    def theme_endpoint() -> Any:
        if request.method == "POST":
            data: Dict[str, Any] = request.get_json() or {}
            return jsonify(
                controllers.apply_theme(state_manager, data.get("theme", "light"))
            )
        return jsonify(controllers.get_theme(state_manager))


def register_fastapi_routes(
    app: FastAPI, state_manager: "StateManager", registry: "ComponentRegistry"
) -> None:
    """Attach route handlers to a FastAPI ``app``."""

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:  # pragma: no cover - simple wrapper
        return controllers.render_index(state_manager)

    @app.get("/api/frontend/state")
    async def get_state() -> Dict[str, Any]:  # pragma: no cover - simple wrapper
        return controllers.current_state(state_manager)

    @app.get("/api/frontend/components")
    async def get_components() -> Dict[str, Any]:  # pragma: no cover - simple wrapper
        return controllers.component_listing(registry)

    @app.post("/api/frontend/state")
    async def update_state(
        updates: Dict[str, Any],
    ) -> Dict[str, Any]:  # pragma: no cover
        return controllers.update_state(state_manager, updates)
