#!/usr/bin/env python3
"""Frontend testing infrastructure.

Provides a unified entry point for running component, routing,
state management and integration tests for the frontend system.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, List, Optional

import pytest

from .frontend_app import (
    FlaskFrontendApp,
    FastAPIFrontendApp,
    FrontendAppFactory,
    ComponentRegistry,
    StateManager,
    UIComponent,
    create_component,
)
from .frontend_router import (
    FrontendRouter,
    RouteConfig,
    NavigationState,
    RouteGuard,
    RouteMiddleware,
    RouteBuilder,
    create_router_with_default_routes,
)
from .component_testing import run_all_component_tests, run_single_component_test
from .routing_testing import run_routing_tests as perform_routing_tests
from .state_testing import run_state_management_tests
from .integration_testing import run_integration_tests as perform_integration_tests
from .testing_models import TestResult, TestSuite
from .testing_utils import MockDataGenerator, TestUtilities

# expose fixtures from testing_utils
pytest_plugins = ["src.web.frontend.testing_utils"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FrontendTestRunner:
    """Main frontend test runner."""

    def __init__(self):
        self.test_results: List[TestResult] = []
        self.test_suites: Dict[str, TestSuite] = {}
        self.current_suite: Optional[TestSuite] = None
        self.mock_data_generator = MockDataGenerator()
        self.test_utilities = TestUtilities()
        logger.info("Frontend test runner initialized")

    def run_component_tests(self, component_name: str = None) -> TestSuite:
        suite_name = f"component_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        suite = TestSuite(
            name=suite_name,
            description="Component testing suite",
            tests=[],
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            skipped_tests=0,
            total_duration=0.0,
            created_at=datetime.now(),
        )
        self.current_suite = suite
        try:
            if component_name:
                run_single_component_test(component_name, suite)
            else:
                run_all_component_tests(suite)
            self._calculate_suite_stats(suite)
            self.test_suites[suite_name] = suite
            logger.info(
                f"Component tests completed: {suite.passed_tests}/{suite.total_tests} passed"
            )
            return suite
        except Exception as e:  # pragma: no cover - safety
            logger.error(f"Error running component tests: {e}")
            raise

    def run_routing_tests(self) -> TestSuite:
        suite_name = f"routing_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        suite = TestSuite(
            name=suite_name,
            description="Routing testing suite",
            tests=[],
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            skipped_tests=0,
            total_duration=0.0,
            created_at=datetime.now(),
        )
        self.current_suite = suite
        try:
            perform_routing_tests(suite)
            self._calculate_suite_stats(suite)
            self.test_suites[suite_name] = suite
            logger.info(
                f"Routing tests completed: {suite.passed_tests}/{suite.total_tests} passed"
            )
            return suite
        except Exception as e:  # pragma: no cover - safety
            logger.error(f"Error running routing tests: {e}")
            raise

    def run_state_tests(self) -> TestSuite:
        suite_name = f"state_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        suite = TestSuite(
            name=suite_name,
            description="State management testing suite",
            tests=[],
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            skipped_tests=0,
            total_duration=0.0,
            created_at=datetime.now(),
        )
        self.current_suite = suite
        try:
            run_state_management_tests(suite)
            self._calculate_suite_stats(suite)
            self.test_suites[suite_name] = suite
            logger.info(
                f"State tests completed: {suite.passed_tests}/{suite.total_tests} passed"
            )
            return suite
        except Exception as e:  # pragma: no cover - safety
            logger.error(f"Error running state tests: {e}")
            raise

    def run_integration_tests(self) -> TestSuite:
        suite_name = f"integration_tests_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        suite = TestSuite(
            name=suite_name,
            description="Integration testing suite",
            tests=[],
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            skipped_tests=0,
            total_duration=0.0,
            created_at=datetime.now(),
        )
        self.current_suite = suite
        try:
            perform_integration_tests(suite)
            self._calculate_suite_stats(suite)
            self.test_suites[suite_name] = suite
            logger.info(
                f"Integration tests completed: {suite.passed_tests}/{suite.total_tests} passed"
            )
            return suite
        except Exception as e:  # pragma: no cover - safety
            logger.error(f"Error running integration tests: {e}")
            raise

    def run_all_tests(self) -> Dict[str, TestSuite]:
        try:
            logger.info("Starting comprehensive frontend testing...")
            component_suite = self.run_component_tests()
            routing_suite = self.run_routing_tests()
            state_suite = self.run_state_tests()
            integration_suite = self.run_integration_tests()
            all_suites = {
                "component": component_suite,
                "routing": routing_suite,
                "state": state_suite,
                "integration": integration_suite,
            }
            self._generate_summary_report(all_suites)
            logger.info("All frontend tests completed")
            return all_suites
        except Exception as e:  # pragma: no cover - safety
            logger.error(f"Error running all tests: {e}")
            raise

    def _calculate_suite_stats(self, suite: TestSuite):
        suite.total_tests = len(suite.tests)
        suite.passed_tests = len([t for t in suite.tests if t.status == "passed"])
        suite.failed_tests = len([t for t in suite.tests if t.status == "failed"])
        suite.skipped_tests = len([t for t in suite.tests if t.status == "skipped"])
        suite.total_duration = sum(t.duration for t in suite.tests)

    def _generate_summary_report(self, suites: Dict[str, TestSuite]):
        total_tests = sum(s.total_tests for s in suites.values())
        total_passed = sum(s.passed_tests for s in suites.values())
        total_failed = sum(s.failed_tests for s in suites.values())
        total_skipped = sum(s.skipped_tests for s in suites.values())
        total_duration = sum(s.total_duration for s in suites.values())

        logger.info("=" * 60)
        logger.info("FRONTEND TESTING SUMMARY REPORT")
        logger.info("=" * 60)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {total_passed}")
        logger.info(f"Failed: {total_failed}")
        logger.info(f"Skipped: {total_skipped}")
        logger.info(f"Total Duration: {total_duration:.2f}s")
        logger.info("=" * 60)
        for suite_name, suite in suites.items():
            logger.info(
                f"{suite_name.upper()}: {suite.passed_tests}/{suite.total_tests} passed"
            )
        logger.info("=" * 60)


# ---------------------------------------------------------------------------
# Pytest test functions
# ---------------------------------------------------------------------------


def test_component_creation(test_utilities):
    component = test_utilities.create_mock_component("TestButton")
    assert component.type == "TestButton"
    assert component.id is not None
    assert component.props["data-testid"] == "test-component"
    assert component.created_at is not None
    assert component.updated_at is not None


def test_route_configuration(test_utilities):
    route = test_utilities.create_mock_route("/test-page")
    test_utilities.assert_route_config(route, "/test-page", "TestComponent")


def test_navigation_state(test_utilities):
    state = test_utilities.create_mock_navigation_state()
    test_utilities.assert_navigation_state(state, "/test")
    assert state.previous_route == "/"
    assert state.route_params["id"] == "123"
    assert len(state.breadcrumbs) == 2


def test_flask_frontend_app(flask_frontend_app):
    assert flask_frontend_app is not None
    assert hasattr(flask_frontend_app, "app")
    assert hasattr(flask_frontend_app, "component_registry")
    assert hasattr(flask_frontend_app, "state_manager")
    registry = flask_frontend_app.component_registry
    assert "Button" in registry.list_components()
    assert "Card" in registry.list_components()


def test_fastapi_frontend_app(fastapi_frontend_app):
    assert fastapi_frontend_app is not None
    assert hasattr(fastapi_frontend_app, "app")
    assert hasattr(fastapi_frontend_app, "component_registry")
    assert hasattr(fastapi_frontend_app, "state_manager")
    registry = fastapi_frontend_app.component_registry
    assert "Button" in registry.list_components()
    assert "Card" in registry.list_components()


def test_frontend_router(frontend_router):
    assert frontend_router is not None
    assert len(frontend_router.routes) > 0
    home_match = frontend_router.match_url("/")
    assert home_match is not None
    assert home_match["matched"] is True
    success = frontend_router.navigate_to("/dashboard")
    assert success is True
    breadcrumbs = frontend_router.get_breadcrumbs()
    assert len(breadcrumbs) > 0


def test_component_registry_integration(flask_frontend_app):
    registry = flask_frontend_app.component_registry
    registry.register_component(
        "CustomComponent", lambda x: x, "template", "style", "script"
    )
    assert "CustomComponent" in registry.list_components()
    component_func = registry.get_component("CustomComponent")
    assert component_func is not None


def test_state_manager_integration(flask_frontend_app):
    state_manager = flask_frontend_app.state_manager
    initial_state = state_manager.get_state()
    assert initial_state.app_name == "Agent_Cellphone_V2 Frontend"
    assert initial_state.theme == "light"
    state_manager.update_state({"theme": "dark"})
    updated_state = state_manager.get_state()
    assert updated_state.theme == "dark"


@pytest.mark.asyncio
async def test_fastapi_websocket_async(fastapi_frontend_app):
    assert fastapi_frontend_app is not None
    assert hasattr(fastapi_frontend_app, "app")


def test_full_frontend_integration(flask_frontend_app, frontend_router):
    app = flask_frontend_app
    router = frontend_router
    registry = app.component_registry
    assert len(registry.list_components()) > 0
    assert len(router.routes) > 0
    state_manager = app.state_manager
    initial_state = state_manager.get_state()
    assert initial_state is not None
    success = router.navigate_to("/dashboard")
    assert success is True
