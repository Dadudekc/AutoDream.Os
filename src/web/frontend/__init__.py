"""
Frontend Package for Agent_Cellphone_V2_Repository
Provides unified frontend application architecture, routing, and testing infrastructure

This package integrates with both Flask and FastAPI backends to provide:
- Component-based UI system
- Real-time communication via WebSockets
- State management and routing
- Comprehensive testing infrastructure
- Responsive design integration

Author: Web Development & UI Framework Specialist
License: MIT
"""

# Core frontend application classes
from .frontend_app import (
    FlaskFrontendApp,
    FastAPIFrontendApp,
    FrontendAppFactory,
    ComponentRegistry,
    StateManager,
    UIComponent,
    create_component,
)

# Frontend routing system
from .frontend_router import (
    FrontendRouter,
    RouteConfig,
    NavigationState,
    RouteGuard,
    RouteMiddleware,
    RouteBuilder,
    create_router_with_default_routes,
    route,
)

# Frontend testing infrastructure
from .frontend_testing import FrontendTestRunner
from .testing_models import TestResult, TestSuite
from .testing_utils import TestUtilities, MockDataGenerator

# Version information
__version__ = "2.0.0"
__author__ = "Agent_Cellphone_V2_Repository Team"
__description__ = "Unified Frontend Application Architecture"

# Package exports
__all__ = [
    # Core application classes
    "FlaskFrontendApp",
    "FastAPIFrontendApp",
    "FrontendAppFactory",
    "ComponentRegistry",
    "StateManager",
    "UIComponent",
    "create_component",
    # Routing system
    "FrontendRouter",
    "RouteConfig",
    "NavigationState",
    "RouteGuard",
    "RouteMiddleware",
    "RouteBuilder",
    "create_router_with_default_routes",
    "route",
    # Testing infrastructure
    "FrontendTestRunner",
    "TestResult",
    "TestSuite",
    "TestUtilities",
    "MockDataGenerator",
]


# Convenience functions for quick setup
def create_flask_frontend(config: dict = None):
    """Quick setup for Flask frontend application"""
    return FrontendAppFactory.create_flask_app(config)


def create_fastapi_frontend(config: dict = None):
    """Quick setup for FastAPI frontend application"""
    return FrontendAppFactory.create_fastapi_app(config)


def create_frontend_router():
    """Quick setup for frontend router with default routes"""
    return create_router_with_default_routes()


def run_frontend_tests():
    """Quick execution of all frontend tests"""
    runner = FrontendTestRunner()
    return runner.run_all_tests()


# Package initialization logging
import logging

from src.utils.stability_improvements import stability_manager, safe_import

logger = logging.getLogger(__name__)
logger.info(f"Frontend package initialized - version {__version__}")
logger.info("Available classes: %s", ", ".join(__all__))
