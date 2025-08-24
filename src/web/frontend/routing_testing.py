"""Routing testing helpers for the frontend."""
from __future__ import annotations

from datetime import datetime

from .frontend_router import create_router_with_default_routes
from .testing_models import TestResult, TestSuite


def run_routing_tests(suite: TestSuite) -> None:
    """Run routing tests and append results to the suite."""
    start_time = datetime.now()
    try:
        router = create_router_with_default_routes()
        assert router is not None
        assert len(router.routes) > 0

        home_match = router.match_url("/")
        assert home_match is not None
        assert home_match["matched"] is True

        success = router.navigate_to("/dashboard")
        assert success is True

        breadcrumbs = router.get_breadcrumbs()
        assert len(breadcrumbs) > 0
        status = "passed"
        error = None
    except Exception as exc:  # pragma: no cover - defensive
        status = "failed"
        error = str(exc)
    duration = (datetime.now() - start_time).total_seconds()
    suite.tests.append(
        TestResult(
            test_name="test_routing_basic",
            test_type="routing",
            status=status,
            duration=duration,
            error_message=error,
            component_tested=None,
            route_tested="/",
            timestamp=datetime.now(),
            metadata={"test_type": "basic_routing"},
        )
    )
