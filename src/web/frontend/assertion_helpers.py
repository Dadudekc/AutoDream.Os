"""Assertion helper functions for frontend tests."""

from typing import Dict, Any

from .frontend_app import UIComponent
from .frontend_router import RouteConfig, NavigationState


def assert_component_props(component: UIComponent, expected_props: Dict[str, Any]) -> None:
    """Assert that a component has the expected properties."""
    for key, value in expected_props.items():
        assert component.props[key] == value, (
            f"Expected {key}={value}, got {component.props.get(key)}"
        )


def assert_route_config(route: RouteConfig, expected_path: str, expected_component: str) -> None:
    """Assert that a route has the expected configuration."""
    assert route.path == expected_path, f"Expected path {expected_path}, got {route.path}"
    assert route.component == expected_component, (
        f"Expected component {expected_component}, got {route.component}"
    )


def assert_navigation_state(state: NavigationState, expected_route: str) -> None:
    """Assert that navigation state matches the expected route."""
    assert state.current_route == expected_route, (
        f"Expected route {expected_route}, got {state.current_route}"
    )
