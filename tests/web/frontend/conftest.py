import pytest

from src.web.frontend.frontend_testing import FrontendTestRunner, MockDataGenerator
from src.web.frontend.frontend_app import FrontendAppFactory
from src.web.frontend.frontend_router import create_router_with_default_routes
from src.web.frontend.ui_interactions import (
    create_mock_component,
    create_mock_route,
    create_mock_navigation_state,
)


@pytest.fixture
def frontend_test_runner():
    return FrontendTestRunner()


@pytest.fixture
def mock_data_generator():
    return MockDataGenerator()


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
def mock_component():
    return create_mock_component()


@pytest.fixture
def mock_route():
    return create_mock_route()


@pytest.fixture
def mock_navigation_state():
    return create_mock_navigation_state()
