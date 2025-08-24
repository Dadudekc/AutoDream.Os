"""Pytest fixtures and mock generators for frontend tests."""
import pytest
from datetime import datetime
from typing import Any, Dict, List

from ..frontend_app import FrontendAppFactory
from ..frontend_router import create_router_with_default_routes
from .ui_utils import UIInteractionUtilities
from .assertion_helpers import AssertionHelpers
from ..frontend_testing import FrontendTestRunner


class MockDataGenerator:
    """Generates mock data for frontend tests."""

    def generate_mock_user(self) -> Dict[str, Any]:
        return {
            "id": "user-123",
            "username": "testuser",
            "email": "test@example.com",
            "role": "user",
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
        }

    def generate_mock_component_data(self, component_type: str) -> Dict[str, Any]:
        base_data = {
            "id": f"{component_type.lower()}-123",
            "className": f"{component_type.lower()}-component",
            "data-testid": f"test-{component_type.lower()}",
        }
        if component_type == "Button":
            base_data.update(
                {"text": "Test Button", "type": "button", "disabled": False}
            )
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
        ]


@pytest.fixture
def ui_utils() -> UIInteractionUtilities:
    return UIInteractionUtilities()


@pytest.fixture
def assertion_helpers() -> AssertionHelpers:
    return AssertionHelpers()


@pytest.fixture
def mock_data_generator() -> MockDataGenerator:
    return MockDataGenerator()


@pytest.fixture
def frontend_test_runner() -> FrontendTestRunner:
    return FrontendTestRunner()


@pytest.fixture
def flask_frontend_app():
    return FrontendAppFactory.create_flask_app()


@pytest.fixture
def fastapi_frontend_app():
    return FrontendAppFactory.create_fastapi_app()


@pytest.fixture
def frontend_router():
    return create_router_with_default_routes()


@pytest.fixture
def mock_component(ui_utils: UIInteractionUtilities):
    return ui_utils.create_mock_component()


@pytest.fixture
def mock_route(ui_utils: UIInteractionUtilities):
    return ui_utils.create_mock_route()


@pytest.fixture
def mock_navigation_state(ui_utils: UIInteractionUtilities):
    return ui_utils.create_mock_navigation_state()
