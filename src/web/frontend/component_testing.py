"""Component testing helpers for the frontend."""
from __future__ import annotations

from datetime import datetime

from .frontend_app import create_component
from .testing_models import TestResult, TestSuite


def run_single_component_test(component_name: str, suite: TestSuite) -> None:
    """Run tests for a single component and append results to the suite."""
    start_time = datetime.now()
    try:
        component = create_component(component_name, {"test": True})
        assert component.type == component_name
        assert component.props["test"] is True
        component.state["test_state"] = "test_value"
        assert component.state["test_state"] == "test_value"
        status = "passed"
        error = None
    except Exception as exc:  # pragma: no cover - defensive
        status = "failed"
        error = str(exc)
    duration = (datetime.now() - start_time).total_seconds()
    suite.tests.append(
        TestResult(
            test_name=f"test_{component_name}_creation",
            test_type="component",
            status=status,
            duration=duration,
            error_message=error,
            component_tested=component_name,
            route_tested=None,
            timestamp=datetime.now(),
            metadata={"test_type": "creation"},
        )
    )


def run_all_component_tests(suite: TestSuite) -> None:
    """Run tests for all basic components."""
    for component_name in ["Button", "Card", "Input", "Modal"]:
        run_single_component_test(component_name, suite)
