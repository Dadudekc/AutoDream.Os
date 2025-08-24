"""Assertion helpers for frontend tests."""
from typing import Dict, Any

from ..frontend_app import UIComponent
from ..frontend_router import RouteConfig, NavigationState


class AssertionHelpers:
    """Provide assertion helper methods for frontend test cases."""

    def assert_component_props(self, component: UIComponent, expected: Dict[str, Any]):
        """Assert that a component has the expected properties."""
        for key, value in expected.items():
            assert (
                component.props[key] == value
            ), f"Expected {key}={value}, got {component.props.get(key)}"

    def assert_route_config(
        self, route: RouteConfig, expected_path: str, expected_component: str
    ):
        """Assert that a route configuration matches expectations."""
        assert (
            route.path == expected_path
        ), f"Expected path {expected_path}, got {route.path}"
        assert (
            route.component == expected_component
        ), f"Expected component {expected_component}, got {route.component}"

    def assert_navigation_state(self, state: NavigationState, expected_route: str):
        """Assert that the navigation state points to the expected route."""
        assert (
            state.current_route == expected_route
        ), f"Expected route {expected_route}, got {state.current_route}"
