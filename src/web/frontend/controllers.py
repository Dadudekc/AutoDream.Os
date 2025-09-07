from typing import Any, Dict, TYPE_CHECKING

    from .frontend_app import ComponentRegistry, StateManager
from .templates import INDEX_HTML
from __future__ import annotations
from dataclasses import asdict
from jinja2 import Template

"""Controller functions for frontend routes.

The controllers operate on generic state and registry objects to allow
use with different web frameworks.
"""





if TYPE_CHECKING:  # pragma: no cover - used only for type hints


def render_index(state_manager: "StateManager") -> str:
    """Return rendered HTML for the index page."""
    template = Template(INDEX_HTML)
    return template.render(app_name=state_manager.get_state().app_name)


def current_state(state_manager: "StateManager") -> Dict[str, Any]:
    """Return current frontend state."""
    return asdict(state_manager.get_state())


def component_listing(registry: "ComponentRegistry") -> Dict[str, Any]:
    """Return available component and template names."""
    return {
        "components": registry.list_components(),
        "templates": list(registry.templates.keys()),
    }


def route_info(route_path: str) -> Dict[str, Any]:
    """Return basic route information for *route_path*."""
    return {"path": f"/{route_path}", "component": "PageComponent", "props": {}}


def apply_theme(state_manager: "StateManager", theme: str) -> Dict[str, str]:
    """Update theme setting and return status."""
    state_manager.update_state({"theme": theme})
    return {"status": "success"}


def get_theme(state_manager: "StateManager") -> Dict[str, str]:
    """Return current theme information."""
    return {"theme": state_manager.get_state().theme}


def update_state(
    state_manager: "StateManager", updates: Dict[str, Any]
) -> Dict[str, str]:
    """Apply *updates* to the global state and report status."""
    try:
        state_manager.update_state(updates)
        return {"status": "success", "message": "State updated"}
    except Exception as exc:  # pragma: no cover - simple error wrapper
        return {"status": "error", "message": str(exc)}
