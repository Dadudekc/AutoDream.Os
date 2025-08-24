"""Shared utilities and fixtures for frontend testing."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import pytest

from .frontend_app import FrontendAppFactory, UIComponent, create_component
from .frontend_router import (
    FrontendRouter,
    NavigationState,
    RouteConfig,
)


class TestUtilities:
    """Utility functions for frontend testing."""

    def create_mock_component(self, component_type: str = "TestComponent") -> UIComponent:
        """Create a mock component for testing."""
        return create_component(
            component_type,
            {
                "id": "test-id",
                "className": "test-class",
                "data-testid": "test-component",
            },
        )

    def create_mock_route(self, path: str = "/test") -> RouteConfig:
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

    def create_mock_navigation_state(self) -> NavigationState:
        """Create a mock navigation state for testing."""
        return NavigationState(
            current_route="/test",
            previous_route="/",
            route_params={"id": "123"},
            query_params={"page": "1"},
            navigation_history=["/", "/test"],
            breadcrumbs=[
                {"path": "/", "name": "Home"},
                {"path": "/test", "name": "Test"},
            ],
            timestamp=datetime.now(),
        )

    def assert_component_props(self, component: UIComponent, expected_props: Dict[str, Any]):
        """Assert component has expected properties."""
        for key, value in expected_props.items():
            assert (
                component.props[key] == value
            ), f"Expected {key}={value}, got {component.props.get(key)}"

    def assert_route_config(self, route: RouteConfig, expected_path: str, expected_component: str):
        """Assert route has expected configuration."""
        assert route.path == expected_path, f"Expected path {expected_path}, got {route.path}"
        assert (
            route.component == expected_component
        ), f"Expected component {expected_component}, got {route.component}"

    def assert_navigation_state(self, state: NavigationState, expected_route: str):
        """Assert navigation state has expected route."""
        assert (
            state.current_route == expected_route
        ), f"Expected route {expected_route}, got {state.current_route}"


class MockDataGenerator:
    """Generates mock data for testing."""

    def generate_mock_user(self) -> Dict[str, Any]:
        """Generate mock user data."""
        return {
            "id": "user-123",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user",
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
        }

    def generate_mock_component_data(self, component_type: str) -> Dict[str, Any]:
        """Generate mock component data."""
        base_data = {
            "id": f"{component_type.lower()}-123",
            "className": f"{component_type.lower()}-component",
            "data-testid": f"test-{component_type.lower()}",
        }
        if component_type == "Button":
            base_data.update({"text": "Test Button", "type": "button", "disabled": False})
        elif component_type == "Card":
            base_data.update(
                {
                    "title": "Test Card",
                    "content": "This is a test card component",
                    "footer": "Card Footer",
                }
            )
        return base_data

    def generate_mock_route_data(self) -> List[Dict[str, Any]]:
        """Generate mock route data."""
        return [
            {
                "path": "/",
                "name": "home",
                "component": "HomePage",
                "props": {"title": "Home"},
                "meta": {"requiresAuth": False},
            },
            {
                "path": "/dashboard",
                "name": "dashboard",
                "component": "DashboardPage",
                "props": {"title": "Dashboard"},
                "meta": {"requiresAuth": True},
            },
            {
                "path": "/settings",
                "name": "settings",
                "component": "SettingsPage",
                "props": {"title": "Settings"},
                "meta": {"requiresAuth": True},
            },
        ]


# ---------------------------------------------------------------------------
# Pytest fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def frontend_test_runner():
    """Fixture for frontend test runner."""
    from .frontend_testing import FrontendTestRunner  # Local import to avoid cycle

    return FrontendTestRunner()


@pytest.fixture
def test_utilities() -> TestUtilities:
    """Fixture for test utilities."""
    return TestUtilities()


@pytest.fixture
def mock_data_generator() -> MockDataGenerator:
    """Fixture for mock data generator."""
    return MockDataGenerator()


@pytest.fixture
def flask_frontend_app():
    """Fixture for Flask frontend app."""
    return FrontendAppFactory.create_flask_app()


@pytest.fixture
def fastapi_frontend_app():
    """Fixture for FastAPI frontend app."""
    return FrontendAppFactory.create_fastapi_app()


@pytest.fixture
def frontend_router():
    """Fixture for frontend router."""
    router = FrontendRouter()
    route = RouteConfig(
        path='/',
        name='home',
        component='HomePage',
        props={},
        meta={},
        children=[],
        guards=[],
        middleware=[],
        lazy_load=False,
        cache=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    dashboard_route = RouteConfig(
        path='/dashboard',
        name='dashboard',
        component='DashboardPage',
        props={},
        meta={},
        children=[],
        guards=[],
        middleware=[],
        lazy_load=False,
        cache=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    router.add_route(dashboard_route)
    router.add_route(route)
    return router
@pytest.fixture
def mock_component(test_utilities: TestUtilities):
    """Fixture for mock component."""
    return test_utilities.create_mock_component()


@pytest.fixture
def mock_route(test_utilities: TestUtilities):
    """Fixture for mock route."""
    return test_utilities.create_mock_route()


@pytest.fixture
def mock_navigation_state(test_utilities: TestUtilities):
    """Fixture for mock navigation state."""
    return test_utilities.create_mock_navigation_state()


__all__ = [
    "TestUtilities",
    "MockDataGenerator",
    "frontend_test_runner",
    "test_utilities",
    "mock_data_generator",
    "flask_frontend_app",
    "fastapi_frontend_app",
    "frontend_router",
    "mock_component",
    "mock_route",
    "mock_navigation_state",
]
