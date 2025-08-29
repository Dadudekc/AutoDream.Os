"""Utilities for simulating frontend UI interactions in tests."""

from ..frontend_app import UIComponent
from ..frontend_router_config import RouteConfig, NavigationState
from ..utils import (
    create_mock_component as _create_mock_component,
    create_mock_route as _create_mock_route,
    create_mock_navigation_state as _create_mock_navigation_state,
)


class UIInteractionUtilities:
    """Create mock frontend entities for testing UI behaviour."""

    def create_mock_component(self, component_type: str = "TestComponent") -> UIComponent:
        """Return a mock :class:`UIComponent` instance."""
        return _create_mock_component(component_type)

    def create_mock_route(self, path: str = "/test") -> RouteConfig:
        """Return a mock :class:`RouteConfig` instance."""
        return _create_mock_route(path)

    def create_mock_navigation_state(self) -> NavigationState:
        """Return a mock :class:`NavigationState` instance."""
        return _create_mock_navigation_state()
