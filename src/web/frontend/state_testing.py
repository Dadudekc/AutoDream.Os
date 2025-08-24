"""State management testing helpers for the frontend."""
from __future__ import annotations

from datetime import datetime

from .frontend_app import FrontendAppFactory
from .testing_models import TestResult, TestSuite


def run_state_management_tests(suite: TestSuite) -> None:
    """Run state management tests and append results to the suite."""
    start_time = datetime.now()
    try:
        app = FrontendAppFactory.create_flask_app()
        state_manager = app.state_manager
        initial_state = state_manager.get_state()
        assert initial_state.app_name == "Agent_Cellphone_V2 Frontend"
        assert initial_state.theme == "light"

        state_manager.update_state({"theme": "dark"})
        updated_state = state_manager.get_state()
        assert updated_state.theme == "dark"
        status = "passed"
        error = None
    except Exception as exc:  # pragma: no cover - defensive
        status = "failed"
        error = str(exc)
    duration = (datetime.now() - start_time).total_seconds()
    suite.tests.append(
        TestResult(
            test_name="test_state_manager",  # rename
            test_type="state",
            status=status,
            duration=duration,
            error_message=error,
            component_tested=None,
            route_tested=None,
            timestamp=datetime.now(),
            metadata={"test_type": "state_management"},
        )
    )
