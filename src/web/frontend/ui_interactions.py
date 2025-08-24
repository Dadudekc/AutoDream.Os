"""UI interaction utilities for frontend tests."""

from datetime import datetime

from .frontend_app import UIComponent, create_component
from .frontend_router import RouteConfig, NavigationState


def create_mock_component(component_type: str = "TestComponent") -> UIComponent:
    """Create a mock UI component for testing."""
    return create_component(
        component_type,
        {
            "id": "test-id",
            "className": "test-class",
            "data-testid": "test-component",
        },
    )


def create_mock_route(path: str = "/test") -> RouteConfig:
    """Create a mock route for testing."""
    return RouteConfig(
        path=path,
        name="test-route",
        component="TestComponent",
        props={"title": "Test Page"},
        meta={"requiresAuth": False},
        children=[],
        guards=[],
        middleware=[],
        lazy_load=False,
        cache=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def create_mock_navigation_state() -> NavigationState:
    """Create a mock navigation state for testing."""
    return NavigationState(
        current_route="/test",
        previous_route="/",
        route_params={"id": "123"},
        query_params={"page": "1"},
        navigation_history=["/", "/test"],
        breadcrumbs=[{"path": "/", "name": "Home"}, {"path": "/test", "name": "Test"}],
        timestamp=datetime.now(),
    )
