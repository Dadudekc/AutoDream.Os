#!/usr/bin/env python3
"""Frontend application orchestrator importing core, routing, and UI modules."""

from typing import Any, Dict

from .frontend_app_core import (
    UIComponent,
    FrontendRoute,
    FrontendState,
    ComponentRegistry,
    StateManager,
)
from .frontend_routing import (
    FlaskFrontendApp,
    FastAPIFrontendApp,
    create_route,
)
from .frontend_ui import (
    create_component,
    register_default_components,
    process_component_event,
)


class FrontendAppFactory:
    """Factory for creating frontend applications."""

    @staticmethod
    def create_flask_app(config: Dict[str, Any] = None) -> FlaskFrontendApp:
        """Create a Flask-based frontend application."""
        return FlaskFrontendApp(config)

    @staticmethod
    def create_fastapi_app(config: Dict[str, Any] = None) -> FastAPIFrontendApp:
        """Create a FastAPI-based frontend application."""
        return FastAPIFrontendApp(config)

    @staticmethod
    def create_unified_app(backend_type: str = "flask", config: Dict[str, Any] = None):
        """Create a unified frontend application."""
        if backend_type.lower() == "fastapi":
            return FrontendAppFactory.create_fastapi_app(config)
        return FrontendAppFactory.create_flask_app(config)


__all__ = [
    "UIComponent",
    "FrontendRoute",
    "FrontendState",
    "ComponentRegistry",
    "StateManager",
    "FlaskFrontendApp",
    "FastAPIFrontendApp",
    "FrontendAppFactory",
    "create_component",
    "register_default_components",
    "process_component_event",
    "create_route",
]


if __name__ == "__main__":
    config = {"debug": True, "secret_key": "development-secret-key"}
    flask_app = FrontendAppFactory.create_flask_app(config)
    fastapi_app = FrontendAppFactory.create_fastapi_app(config)
    print("Frontend applications created successfully!")
    print(f"Flask app: {flask_app}")
    print(f"FastAPI app: {fastapi_app}")
