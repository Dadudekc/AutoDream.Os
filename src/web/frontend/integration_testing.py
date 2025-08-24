"""Integration testing helpers for the frontend."""
from __future__ import annotations

from datetime import datetime

from .frontend_app import FrontendAppFactory
from .testing_models import TestResult, TestSuite


def run_integration_tests(suite: TestSuite) -> None:
    """Run integration tests and append results to the suite."""
    start_time = datetime.now()
    try:
        flask_app = FrontendAppFactory.create_flask_app()
        assert flask_app is not None
        assert hasattr(flask_app, "app")
        assert hasattr(flask_app, "component_registry")

        fastapi_app = FrontendAppFactory.create_fastapi_app()
        assert fastapi_app is not None
        assert hasattr(fastapi_app, "app")
        assert hasattr(fastapi_app, "component_registry")

        registry = flask_app.component_registry
        registry.register_component("TestComponent", lambda x: x)
        assert "TestComponent" in registry.list_components()
        status = "passed"
        error = None
    except Exception as exc:  # pragma: no cover - defensive
        status = "failed"
        error = str(exc)
    duration = (datetime.now() - start_time).total_seconds()
    suite.tests.append(
        TestResult(
            test_name="test_integration_apps",
            test_type="integration",
            status=status,
            duration=duration,
            error_message=error,
            component_tested=None,
            route_tested=None,
            timestamp=datetime.now(),
            metadata={"test_type": "app_integration"},
        )
    )
